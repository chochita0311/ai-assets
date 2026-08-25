#!/usr/bin/env python3
"""Validate, publish, and safely maintain one skill-owned GitHub PR review."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = 2
SUPPORTED_MARKER_VERSIONS = {"1", "2"}
MAX_COMMENTS = 8
REVIEW_PROFILES = {"focused", "balanced", "assertive"}
MAX_REVIEW_NOTES = {"focused": 0, "balanced": 3, "assertive": 5}
EVIDENCE_AREA_LABELS = {
    "boundary-behavior": "Boundary / behavior",
    "integration-consumers": "Integration / consumers",
    "tests-validation": "Tests / validation",
    "design-adversarial": "Design / adversarial",
    "independence": "Independence",
}
FINAL_STATES = {"COMMENTED", "APPROVED", "CHANGES_REQUESTED"}
EVENT_STATES = {
    "COMMENT": "COMMENTED",
    "APPROVE": "APPROVED",
    "REQUEST_CHANGES": "CHANGES_REQUESTED",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
THREAD_HEADER_RE = re.compile(
    r"^(issue|suggestion) \((blocking|non-blocking|question), "
    r"(critical|high|medium|low), ([a-z0-9][a-z0-9-]{2,79})\): \S.+$"
)
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
REVIEW_MARKER_RE = re.compile(
    r"<!--\s*gh-review-pr:review\s+v=(?P<version>\d+)\s+"
    r"base=(?P<base>[0-9a-f]+)\s+head=(?P<head>[0-9a-f]+)\s+"
    r"run=(?P<run>[0-9a-f]+)\s*-->"
)
FINDING_MARKER_RE = re.compile(
    r"<!--\s*gh-review-pr:finding\s+v=(?P<version>\d+)\s+"
    r"base=(?P<base>[0-9a-f]+)\s+head=(?P<head>[0-9a-f]+)\s+"
    r"run=(?P<run>[0-9a-f]+)\s+id=(?P<finding>[a-z0-9-]+)\s*-->"
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)\b"
        r"\s*[:=]\s*(['\"])[^'\"\s]{12,}\1"
    ),
)


class TransactionError(Exception):
    """Base class for sanitized command failures."""

    code = "transaction-error"
    exit_code = 3


class PlanError(TransactionError):
    code = "invalid-plan"
    exit_code = 2


class SafetyError(TransactionError):
    code = "safety-stop"
    exit_code = 3


class GitHubError(TransactionError):
    code = "github-error"
    exit_code = 4

    def __init__(self, message: str, *, ambiguous_write: bool = False) -> None:
        super().__init__(message)
        self.ambiguous_write = ambiguous_write


class VerificationError(TransactionError):
    code = "verification-failed"
    exit_code = 5


class JsonArgumentParser(argparse.ArgumentParser):
    """Convert command-line usage errors into the sanitized JSON error contract."""

    def error(self, message: str) -> None:
        raise PlanError(f"CLI argument error: {message}")


@dataclass(frozen=True)
class PullRequestRef:
    url: str
    host: str
    owner: str
    repo: str
    number: int

    @property
    def repository(self) -> str:
        return f"{self.owner}/{self.repo}"

    @property
    def endpoint(self) -> str:
        return f"repos/{self.owner}/{self.repo}/pulls/{self.number}"

    @classmethod
    def parse(cls, value: str) -> PullRequestRef:
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.hostname:
            raise PlanError("PR target must be a full HTTPS URL")
        if (
            parsed.username
            or parsed.password
            or parsed.port
            or parsed.query
            or parsed.fragment
        ):
            raise PlanError(
                "PR URL must not contain credentials, a port, query, or fragment"
            )
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) != 4 or parts[2] != "pull" or not parts[3].isdigit():
            raise PlanError(
                "PR URL must match https://<host>/<owner>/<repo>/pull/<number>"
            )
        owner, repo = parts[0], parts[1]
        if not NAME_RE.fullmatch(owner) or not NAME_RE.fullmatch(repo):
            raise PlanError("PR owner and repository contain unsupported characters")
        number = int(parts[3])
        if number < 1:
            raise PlanError("PR number must be positive")
        canonical = f"https://{parsed.hostname}/{owner}/{repo}/pull/{number}"
        return cls(canonical, parsed.hostname.lower(), owner, repo, number)


@dataclass(frozen=True)
class CommentPlan:
    finding_id: str
    path: str
    line: int
    side: str
    severity: str
    confidence: str
    disposition: str
    category: str
    body: str

    def rendered_body(self, plan: ReviewPlan) -> str:
        marker = finding_marker(plan, self.finding_id)
        return f"{self.body}\n\n{marker}"


@dataclass(frozen=True)
class ReviewNote:
    label: str
    text: str

    def as_dict(self) -> Mapping[str, str]:
        return {"label": self.label, "text": self.text}


@dataclass(frozen=True)
class ReviewEvidence:
    area: str
    detail: str

    def as_dict(self) -> Mapping[str, str]:
        return {"area": self.area, "detail": self.detail}


@dataclass(frozen=True)
class ReviewSummary:
    overview: str
    scope: str
    focus: tuple[str, ...]
    evidence: tuple[ReviewEvidence, ...]
    coverage_gaps: tuple[str, ...]
    review_notes: tuple[ReviewNote, ...]

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "overview": self.overview,
            "scope": self.scope,
            "focus": list(self.focus),
            "evidence": [item.as_dict() for item in self.evidence],
            "coverage_gaps": list(self.coverage_gaps),
            "review_notes": [note.as_dict() for note in self.review_notes],
        }


@dataclass(frozen=True)
class ReviewPlan:
    base_sha: str
    head_sha: str
    profile: str
    summary: ReviewSummary
    comments: tuple[CommentPlan, ...]

    @property
    def run_id(self) -> str:
        material = {
            "schema_version": SCHEMA_VERSION,
            "base_sha": self.base_sha,
            "head_sha": self.head_sha,
            "profile": self.profile,
            "summary": self.summary.as_dict(),
            "comments": [comment.__dict__ for comment in self.comments],
        }
        encoded = json.dumps(
            material, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()[:24]

    def summary_body(self) -> str:
        counts = {
            disposition: sum(
                comment.disposition == disposition and comment.severity != "low"
                for comment in self.comments
            )
            for disposition in ("blocking", "non-blocking", "question")
        }
        suggestion_count = sum(comment.severity == "low" for comment in self.comments)
        finding_counts = " · ".join(
            (
                emphasized_count(counts["blocking"], "blocking"),
                emphasized_count(counts["non-blocking"], "non-blocking"),
                emphasized_count(counts["question"], "question", "questions"),
                emphasized_count(suggestion_count, "suggestion", "suggestions"),
            )
        )
        gap_count = len(self.summary.coverage_gaps)
        lines = [
            "## Review summary",
            "",
            self.summary.overview,
            "",
            "### Review receipt",
            "",
            "| Item | Result |",
            "| --- | --- |",
            f"| Profile | `{self.profile}` |",
            f"| Snapshot | `{self.head_sha[:7]}` |",
            f"| Scope | {markdown_table_cell(self.summary.scope)} |",
            f"| Focus | {markdown_table_cell('; '.join(self.summary.focus))} |",
            f"| Findings | {finding_counts} |",
            "| Coverage gaps | "
            + (
                f"{gap_count} recorded; see warning below."
                if gap_count
                else "None recorded."
            )
            + " |",
        ]
        if gap_count:
            gap_label = "Coverage gap" if gap_count == 1 else "Coverage gaps"
            lines.extend(
                (
                    "",
                    "> [!WARNING]",
                    f"> **{gap_label}:**",
                    ">",
                )
            )
            lines.extend(f"> - {gap}" for gap in self.summary.coverage_gaps)
        lines.extend(("", "### Review evidence", ""))
        lines.extend(
            f"- **{EVIDENCE_AREA_LABELS[item.area]}** — {item.detail}"
            for item in self.summary.evidence
        )
        if self.summary.review_notes:
            lines.extend(("", "### Review notes", ""))
            labels = {"optional": "Optional", "fyi": "FYI", "positive": "Positive"}
            lines.extend(
                f"- **{labels[note.label]}** — {note.text}"
                for note in self.summary.review_notes
            )
        return "\n".join(lines)

    def rendered_summary(self) -> str:
        return f"{self.summary_body()}\n\n{review_marker(self)}"


@dataclass(frozen=True)
class AmendmentPlan:
    base_sha: str
    head_sha: str
    review_id: int
    finding_id: str
    body: str


@dataclass(frozen=True)
class ReplyPlan:
    base_sha: str
    head_sha: str
    review_id: int
    finding_id: str
    body: str


@dataclass
class RemoteState:
    pull: Mapping[str, Any]
    files: list[Mapping[str, Any]]
    reviews: list[Mapping[str, Any]]
    comments: list[Mapping[str, Any]]
    current_login: str

    @property
    def base_sha(self) -> str:
        return nested_string(self.pull, "base", "sha")

    @property
    def head_sha(self) -> str:
        return nested_string(self.pull, "head", "sha")


@dataclass(frozen=True)
class Preflight:
    status: str
    state: RemoteState
    review_id: int | None = None
    review_url: str | None = None


def ensure_exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if unknown:
            details.append(f"unknown {', '.join(unknown)}")
        raise PlanError(f"{label} has {'; '.join(details)}")


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlanError(f"{label} must be a non-empty string")
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def reject_secret_literals(text: str, label: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise PlanError(f"{label} appears to contain a secret literal; redact it")


def validate_profile(value: Any) -> str:
    profile = require_string(value, "profile").lower()
    if profile not in REVIEW_PROFILES:
        raise PlanError("profile must be focused, balanced, or assertive")
    return profile


def markdown_table_cell(value: str) -> str:
    """Keep validated one-line content inside one GitHub Markdown table cell."""
    return value.replace("|", r"\|")


def emphasized_count(count: int, singular: str, plural: str | None = None) -> str:
    """Emphasize only nonzero finding counts so exceptions remain scannable."""
    label = singular if count == 1 else plural or singular
    rendered = f"{count} {label}"
    return f"**{rendered}**" if count else rendered


def validate_summary_text(value: Any, label: str, *, max_length: int) -> str:
    text = require_string(value, label)
    if "\n" in text:
        raise PlanError(f"{label} must be one line")
    if len(text) > max_length:
        raise PlanError(f"{label} must be at most {max_length} characters")
    if "gh-review-pr:" in text.lower():
        raise PlanError(f"{label} must not contain a pre-existing skill marker")
    if "<!--" in text or "-->" in text or re.match(
        r"^(?:#{1,6}\s|[-*+>]\s|\d+\.\s|`{3,}|~{3,}|-{3,}|\*{3,}|_{3,}|</?[A-Za-z][^>]*>)",
        text,
    ):
        raise PlanError(f"{label} must be plain one-line content")
    reject_secret_literals(text, label)
    return text


def validate_summary_list(
    value: Any,
    label: str,
    *,
    minimum: int,
    maximum: int,
    item_max_length: int,
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PlanError(f"{label} must be an array")
    if not minimum <= len(value) <= maximum:
        raise PlanError(
            f"{label} must contain between {minimum} and {maximum} items"
        )
    items = tuple(
        validate_summary_text(item, f"{label}[{index}]", max_length=item_max_length)
        for index, item in enumerate(value)
    )
    if len(items) != len(set(items)):
        raise PlanError(f"{label} must not contain duplicate items")
    return items


def validate_review_notes(value: Any, profile: str) -> tuple[ReviewNote, ...]:
    if not isinstance(value, list):
        raise PlanError("summary.review_notes must be an array")
    maximum = MAX_REVIEW_NOTES[profile]
    if len(value) > maximum:
        raise PlanError(
            f"summary.review_notes may contain at most {maximum} items for {profile}"
        )
    notes = []
    for index, raw_note in enumerate(value):
        label = f"summary.review_notes[{index}]"
        if not isinstance(raw_note, Mapping):
            raise PlanError(f"{label} must be an object")
        ensure_exact_keys(raw_note, {"label", "text"}, label)
        note_label = require_string(raw_note["label"], f"{label}.label").lower()
        if note_label not in {"optional", "fyi", "positive"}:
            raise PlanError(f"{label}.label must be optional, fyi, or positive")
        text = validate_summary_text(
            raw_note["text"], f"{label}.text", max_length=240
        )
        if THREAD_HEADER_RE.fullmatch(text):
            raise PlanError(f"{label}.text must not masquerade as an inline thread")
        notes.append(ReviewNote(note_label, text))
    if len({(note.label, note.text) for note in notes}) != len(notes):
        raise PlanError("summary.review_notes must not contain duplicates")
    return tuple(notes)


def validate_review_evidence(value: Any) -> tuple[ReviewEvidence, ...]:
    if not isinstance(value, list):
        raise PlanError("summary.evidence must be an array")
    if not 2 <= len(value) <= len(EVIDENCE_AREA_LABELS):
        raise PlanError(
            "summary.evidence must contain between 2 and "
            f"{len(EVIDENCE_AREA_LABELS)} items"
        )
    evidence = []
    for index, raw_item in enumerate(value):
        label = f"summary.evidence[{index}]"
        if not isinstance(raw_item, Mapping):
            raise PlanError(f"{label} must be an object")
        ensure_exact_keys(raw_item, {"area", "detail"}, label)
        area = require_string(raw_item["area"], f"{label}.area").lower()
        if area not in EVIDENCE_AREA_LABELS:
            allowed = ", ".join(sorted(EVIDENCE_AREA_LABELS))
            raise PlanError(f"{label}.area must be one of: {allowed}")
        detail = validate_summary_text(
            raw_item["detail"], f"{label}.detail", max_length=320
        )
        evidence.append(ReviewEvidence(area, detail))
    areas = [item.area for item in evidence]
    if len(areas) != len(set(areas)):
        raise PlanError("summary.evidence areas must be unique")
    return tuple(evidence)


def validate_summary(value: Any, profile: str) -> ReviewSummary:
    if not isinstance(value, Mapping):
        raise PlanError("summary must be an object")
    ensure_exact_keys(
        value,
        {
            "overview",
            "scope",
            "focus",
            "evidence",
            "coverage_gaps",
            "review_notes",
        },
        "summary",
    )
    return ReviewSummary(
        overview=validate_summary_text(
            value["overview"], "summary.overview", max_length=600
        ),
        scope=validate_summary_text(value["scope"], "summary.scope", max_length=400),
        focus=validate_summary_list(
            value["focus"],
            "summary.focus",
            minimum=1,
            maximum=4,
            item_max_length=120,
        ),
        evidence=validate_review_evidence(value["evidence"]),
        coverage_gaps=validate_summary_list(
            value["coverage_gaps"],
            "summary.coverage_gaps",
            minimum=0,
            maximum=4,
            item_max_length=240,
        ),
        review_notes=validate_review_notes(value["review_notes"], profile),
    )


def validate_sha(value: Any, label: str) -> str:
    sha = require_string(value, label).lower()
    if not SHA_RE.fullmatch(sha):
        raise PlanError(f"{label} must be a full 40- or 64-character hexadecimal SHA")
    return sha


def validate_path(value: Any, label: str) -> str:
    path = require_string(value, label)
    pure = PurePosixPath(path)
    if path.startswith("/") or "\\" in path or "\x00" in path or ".." in pure.parts:
        raise PlanError(f"{label} must be a repository-relative POSIX path")
    if str(pure) != path or path in {".", ""}:
        raise PlanError(f"{label} must be a normalized repository-relative path")
    return path


def parse_comment(value: Any, index: int, profile: str = "balanced") -> CommentPlan:
    label = f"comments[{index}]"
    if not isinstance(value, Mapping):
        raise PlanError(f"{label} must be an object")
    expected = {
        "finding_id",
        "path",
        "line",
        "side",
        "severity",
        "confidence",
        "disposition",
        "category",
        "body",
    }
    ensure_exact_keys(value, expected, label)
    finding_id = require_string(value["finding_id"], f"{label}.finding_id")
    if not SLUG_RE.fullmatch(finding_id):
        raise PlanError(f"{label}.finding_id must be a 3-80 character lowercase slug")
    path = validate_path(value["path"], f"{label}.path")
    line = value["line"]
    if isinstance(line, bool) or not isinstance(line, int) or line < 1:
        raise PlanError(f"{label}.line must be a positive integer")
    side = require_string(value["side"], f"{label}.side").upper()
    if side not in {"LEFT", "RIGHT"}:
        raise PlanError(f"{label}.side must be LEFT or RIGHT")
    severity = require_string(value["severity"], f"{label}.severity").lower()
    allowed_severities = {"critical", "high", "medium"}
    if profile == "assertive":
        allowed_severities.add("low")
    if severity not in allowed_severities:
        allowed = ", ".join(sorted(allowed_severities))
        raise PlanError(f"{label}.severity must be one of: {allowed}")
    confidence = require_string(value["confidence"], f"{label}.confidence").lower()
    if confidence != "high":
        raise PlanError(f"{label}.confidence must be high for publication")
    disposition = require_string(value["disposition"], f"{label}.disposition").lower()
    if disposition not in {"blocking", "non-blocking", "question"}:
        raise PlanError(
            f"{label}.disposition must be blocking, non-blocking, or question"
        )
    category = require_string(value["category"], f"{label}.category").lower()
    if not SLUG_RE.fullmatch(category):
        raise PlanError(f"{label}.category must be a lowercase slug")
    body = require_string(value["body"], f"{label}.body")
    if len(body) > 4000:
        raise PlanError(f"{label}.body must be at most 4000 characters")
    if "gh-review-pr:" in body.lower():
        raise PlanError(f"{label}.body must not contain a pre-existing skill marker")
    if severity == "low" and disposition != "non-blocking":
        raise PlanError(
            f"{label} low-severity suggestions must use non-blocking disposition"
        )
    thread_kind = "suggestion" if severity == "low" else "issue"
    expected_prefix = f"{thread_kind} ({disposition}, {severity}, {category}): "
    first_line = body.splitlines()[0]
    if not first_line.startswith(expected_prefix) or len(first_line) == len(
        expected_prefix
    ):
        raise PlanError(f"{label}.body first line must start with {expected_prefix!r}")
    nonempty_lines = [
        line_value for line_value in body.splitlines() if line_value.strip()
    ]
    if len(nonempty_lines) < 2:
        raise PlanError(f"{label}.body must include evidence, impact, or a safe path")
    reject_secret_literals(body, f"{label}.body")
    return CommentPlan(
        finding_id,
        path,
        line,
        side,
        severity,
        confidence,
        disposition,
        category,
        body,
    )


def load_plan(path: Path) -> ReviewPlan:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise PlanError(f"cannot read plan file: {error}") from error
    except json.JSONDecodeError as error:
        raise PlanError(
            f"plan is not valid JSON: line {error.lineno}, column {error.colno}"
        ) from error
    if not isinstance(raw, Mapping):
        raise PlanError("plan root must be an object")
    ensure_exact_keys(
        raw,
        {
            "schema_version",
            "base_sha",
            "head_sha",
            "profile",
            "summary",
            "comments",
        },
        "plan",
    )
    if raw["schema_version"] != SCHEMA_VERSION:
        raise PlanError(f"schema_version must be {SCHEMA_VERSION}")
    base_sha = validate_sha(raw["base_sha"], "base_sha")
    head_sha = validate_sha(raw["head_sha"], "head_sha")
    if base_sha == head_sha:
        raise PlanError("base_sha and head_sha must differ")
    profile = validate_profile(raw["profile"])
    summary = validate_summary(raw["summary"], profile)
    raw_comments = raw["comments"]
    if not isinstance(raw_comments, list):
        raise PlanError("comments must be an array")
    if len(raw_comments) > MAX_COMMENTS:
        raise PlanError(f"comments must contain at most {MAX_COMMENTS} inline threads")
    comments = tuple(
        parse_comment(value, index, profile)
        for index, value in enumerate(raw_comments)
    )
    finding_ids = [comment.finding_id for comment in comments]
    if len(finding_ids) != len(set(finding_ids)):
        raise PlanError("finding_id values must be unique")
    anchors = [(comment.path, comment.line, comment.side) for comment in comments]
    if len(anchors) != len(set(anchors)):
        raise PlanError("each inline anchor may be used only once")
    plan = ReviewPlan(base_sha, head_sha, profile, summary, comments)
    validate_summary_facts(plan)
    return plan


def validate_amendment_body(value: Any) -> str:
    body = require_string(value, "amendment.body")
    if len(body) > 4000:
        raise PlanError("amendment.body must be at most 4000 characters")
    if "gh-review-pr:" in body.lower():
        raise PlanError("amendment.body must not contain a skill marker")
    if issue_classification(body) is None:
        raise PlanError(
            "amendment.body must start with a valid issue or suggestion "
            "disposition, severity, and category"
        )
    if len([line for line in body.splitlines() if line.strip()]) < 2:
        raise PlanError("amendment.body must include evidence, impact, or a safe path")
    reject_secret_literals(body, "amendment.body")
    return body


def issue_classification(value: Any) -> tuple[str, str, str, str] | None:
    if not isinstance(value, str) or not value.splitlines():
        return None
    match = THREAD_HEADER_RE.fullmatch(value.splitlines()[0])
    if not match:
        return None
    kind, disposition, severity, category = match.groups()
    if severity == "low":
        if kind != "suggestion" or disposition != "non-blocking":
            return None
    elif kind != "issue":
        return None
    return kind, disposition, severity, category


def load_amendment(path: Path) -> AmendmentPlan:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise PlanError(f"cannot read amendment file: {error}") from error
    except json.JSONDecodeError as error:
        raise PlanError(
            f"amendment is not valid JSON: line {error.lineno}, column {error.colno}"
        ) from error
    if not isinstance(raw, Mapping):
        raise PlanError("amendment root must be an object")
    ensure_exact_keys(
        raw,
        {
            "schema_version",
            "base_sha",
            "head_sha",
            "review_id",
            "finding_id",
            "body",
        },
        "amendment",
    )
    if raw["schema_version"] != SCHEMA_VERSION:
        raise PlanError(f"schema_version must be {SCHEMA_VERSION}")
    review_id = raw["review_id"]
    if isinstance(review_id, bool) or not isinstance(review_id, int) or review_id < 1:
        raise PlanError("amendment.review_id must be a positive integer")
    finding_id = require_string(raw["finding_id"], "amendment.finding_id").lower()
    if not SLUG_RE.fullmatch(finding_id):
        raise PlanError("amendment.finding_id must be a lowercase slug")
    return AmendmentPlan(
        validate_sha(raw["base_sha"], "base_sha"),
        validate_sha(raw["head_sha"], "head_sha"),
        review_id,
        finding_id,
        validate_amendment_body(raw["body"]),
    )


def validate_reply_body(value: Any) -> str:
    body = require_string(value, "reply.body")
    if len(body) > 4000:
        raise PlanError("reply.body must be at most 4000 characters")
    if "gh-review-pr:" in body.lower():
        raise PlanError("reply.body must not contain a skill marker")
    reject_secret_literals(body, "reply.body")
    return body


def load_reply(path: Path) -> ReplyPlan:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise PlanError(f"cannot read reply file: {error}") from error
    except json.JSONDecodeError as error:
        raise PlanError(
            f"reply is not valid JSON: line {error.lineno}, column {error.colno}"
        ) from error
    if not isinstance(raw, Mapping):
        raise PlanError("reply root must be an object")
    ensure_exact_keys(
        raw,
        {
            "schema_version",
            "base_sha",
            "head_sha",
            "review_id",
            "finding_id",
            "body",
        },
        "reply",
    )
    if raw["schema_version"] != SCHEMA_VERSION:
        raise PlanError(f"schema_version must be {SCHEMA_VERSION}")
    review_id = raw["review_id"]
    if isinstance(review_id, bool) or not isinstance(review_id, int) or review_id < 1:
        raise PlanError("reply.review_id must be a positive integer")
    finding_id = require_string(raw["finding_id"], "reply.finding_id").lower()
    if not SLUG_RE.fullmatch(finding_id):
        raise PlanError("reply.finding_id must be a lowercase slug")
    return ReplyPlan(
        validate_sha(raw["base_sha"], "base_sha"),
        validate_sha(raw["head_sha"], "head_sha"),
        review_id,
        finding_id,
        validate_reply_body(raw["body"]),
    )


def validate_summary_facts(plan: ReviewPlan) -> None:
    has_material_finding = any(
        comment.severity != "low" for comment in plan.comments
    )
    if not has_material_finding and len(plan.summary.evidence) < 3:
        raise PlanError(
            "summaries without material issue findings must contain at least "
            "three evidence entries"
        )
    checkmark_count = json.dumps(
        plan.summary.as_dict(), ensure_ascii=False
    ).count("✅")
    validation_evidence = next(
        (
            item.detail
            for item in plan.summary.evidence
            if item.area == "tests-validation"
        ),
        "",
    )
    if checkmark_count > 1 or (
        checkmark_count == 1 and not validation_evidence.endswith("✅")
    ):
        raise PlanError(
            "summary may contain at most one ✅, only as the final status cue "
            "in tests-validation evidence"
        )
    rendered = plan.summary_body()
    if len(rendered) > 5000:
        raise PlanError("rendered summary must be at most 5000 characters")
    reject_secret_literals(rendered, "rendered summary")
    for comment in plan.comments:
        title = comment.body.splitlines()[0].split(": ", 1)[1]
        if title in rendered:
            raise PlanError(
                f"summary must not repeat the inline title for {comment.finding_id}"
            )


def review_marker(plan: ReviewPlan) -> str:
    return (
        f"<!-- gh-review-pr:review v={SCHEMA_VERSION} base={plan.base_sha} "
        f"head={plan.head_sha} run={plan.run_id} -->"
    )


def finding_marker(plan: ReviewPlan, finding_id: str) -> str:
    return (
        f"<!-- gh-review-pr:finding v={SCHEMA_VERSION} base={plan.base_sha} "
        f"head={plan.head_sha} run={plan.run_id} id={finding_id} -->"
    )


def marker_match(pattern: re.Pattern[str], body: Any) -> Mapping[str, str] | None:
    if not isinstance(body, str):
        return None
    matches = list(pattern.finditer(body))
    if len(matches) != 1:
        return None
    return matches[0].groupdict()


def review_marker_data(body: Any) -> Mapping[str, str] | None:
    return marker_match(REVIEW_MARKER_RE, body)


def finding_marker_data(body: Any) -> Mapping[str, str] | None:
    return marker_match(FINDING_MARKER_RE, body)


def is_supported_marker(marker: Mapping[str, str] | None) -> bool:
    return bool(marker and marker.get("version") in SUPPORTED_MARKER_VERSIONS)


def without_marker(body: Any, pattern: re.Pattern[str]) -> str:
    if not isinstance(body, str):
        return ""
    return pattern.sub("", body).strip().replace("\r\n", "\n").replace("\r", "\n")


def changed_anchors(patch: str) -> set[tuple[int, str]]:
    anchors: set[tuple[int, str]] = set()
    old_line = 0
    new_line = 0
    in_hunk = False
    for patch_line in patch.splitlines():
        hunk = HUNK_RE.match(patch_line)
        if hunk:
            old_line = int(hunk.group(1))
            new_line = int(hunk.group(2))
            in_hunk = True
            continue
        if not in_hunk or patch_line.startswith("\\"):
            continue
        if patch_line.startswith("+"):
            anchors.add((new_line, "RIGHT"))
            new_line += 1
        elif patch_line.startswith("-"):
            anchors.add((old_line, "LEFT"))
            old_line += 1
        elif patch_line.startswith(" "):
            old_line += 1
            new_line += 1
        else:
            in_hunk = False
    return anchors


def legacy_position_for_anchor(patch: str, line: int, side: str) -> int | None:
    """Map an exact blob-line anchor to GitHub's legacy diff position."""
    old_line = 0
    new_line = 0
    position = 0
    in_hunk = False
    for patch_line in patch.splitlines():
        hunk = HUNK_RE.match(patch_line)
        if hunk:
            if in_hunk:
                position += 1
            old_line = int(hunk.group(1))
            new_line = int(hunk.group(2))
            in_hunk = True
            continue
        if not in_hunk:
            continue
        position += 1
        if patch_line.startswith("+"):
            if side == "RIGHT" and new_line == line:
                return position
            new_line += 1
        elif patch_line.startswith("-"):
            if side == "LEFT" and old_line == line:
                return position
            old_line += 1
        elif patch_line.startswith(" "):
            old_line += 1
            new_line += 1
    return None


def nested_string(value: Mapping[str, Any], *keys: str) -> str:
    current: Any = value
    for key in keys:
        if not isinstance(current, Mapping):
            return ""
        current = current.get(key)
    return current if isinstance(current, str) else ""


def integer_id(value: Mapping[str, Any], label: str) -> int:
    candidate = value.get("id")
    if isinstance(candidate, bool) or not isinstance(candidate, int):
        raise VerificationError(f"{label} did not return an integer id")
    return candidate


def sanitize_remote_error(text: str) -> str:
    cleaned = text.strip().replace("\r", " ").replace("\n", " ")
    cleaned = re.sub(
        r"(?i)(authorization:\s*(?:bearer|token)\s+)\S+", r"\1[REDACTED]", cleaned
    )
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("[REDACTED]", cleaned)
    return cleaned[:800] or "gh returned an unspecified error"


class GitHubClient:
    def __init__(self, host: str, timeout: int = 60) -> None:
        gh = shutil.which("gh")
        if not gh:
            raise GitHubError("gh CLI was not found on PATH")
        self.gh = gh
        self.host = host
        self.timeout = timeout

    def request(
        self, method: str, endpoint: str, payload: Mapping[str, Any] | None = None
    ) -> Any:
        command = [
            self.gh,
            "api",
            "--hostname",
            self.host,
            "--method",
            method,
            endpoint,
        ]
        input_text = None
        if payload is not None:
            command.extend(["--input", "-"])
            input_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        environment = os.environ.copy()
        environment["GH_HOST"] = self.host
        try:
            result = subprocess.run(
                command,
                input=input_text,
                text=True,
                capture_output=True,
                timeout=self.timeout,
                env=environment,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise GitHubError(
                f"gh {method} timed out for {endpoint}",
                ambiguous_write=method != "GET",
            ) from error
        if result.returncode != 0:
            detail = sanitize_remote_error(result.stderr or result.stdout)
            raise GitHubError(
                f"gh {method} failed for {endpoint}: {detail}",
                ambiguous_write=method != "GET",
            )
        if not result.stdout.strip():
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise GitHubError(f"gh returned invalid JSON for {endpoint}") from error

    def get(self, endpoint: str) -> Any:
        return self.request("GET", endpoint)

    def post(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        return self.request("POST", endpoint, payload)

    def patch(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        return self.request("PATCH", endpoint, payload)

    def delete(self, endpoint: str) -> Any:
        return self.request("DELETE", endpoint)

    def paginate(self, endpoint: str) -> list[Mapping[str, Any]]:
        values: list[Mapping[str, Any]] = []
        separator = "&" if "?" in endpoint else "?"
        for page in range(1, 1001):
            result = self.get(f"{endpoint}{separator}per_page=100&page={page}")
            if not isinstance(result, list):
                raise GitHubError(f"gh expected an array from {endpoint}")
            if not all(isinstance(item, Mapping) for item in result):
                raise GitHubError(f"gh returned malformed array data from {endpoint}")
            values.extend(result)
            if len(result) < 100:
                return values
        raise GitHubError(f"pagination exceeded 1000 pages for {endpoint}")


def fetch_state(
    client: GitHubClient, ref: PullRequestRef, *, include_files: bool
) -> RemoteState:
    pull = client.get(ref.endpoint)
    user = client.get("user")
    if not isinstance(pull, Mapping) or not isinstance(user, Mapping):
        raise GitHubError("GitHub returned malformed PR or user metadata")
    login = user.get("login")
    if not isinstance(login, str) or not login:
        raise GitHubError("GitHub did not return the authenticated user login")
    files = client.paginate(f"{ref.endpoint}/files") if include_files else []
    reviews = client.paginate(f"{ref.endpoint}/reviews")
    comments = client.paginate(f"{ref.endpoint}/comments")
    state = RemoteState(pull, files, reviews, comments, login)
    if not SHA_RE.fullmatch(state.base_sha) or not SHA_RE.fullmatch(state.head_sha):
        raise GitHubError("GitHub returned missing or non-full base/head SHAs")
    return state


def authenticated_login(client: GitHubClient) -> str:
    user = client.get("user")
    if not isinstance(user, Mapping) or not isinstance(user.get("login"), str):
        raise GitHubError("GitHub did not return the authenticated user login")
    login = user["login"]
    if not login:
        raise GitHubError("GitHub returned an empty authenticated user login")
    return login


def audit_result(ref: PullRequestRef, state: RemoteState) -> Mapping[str, Any]:
    owned_reviews = []
    human_pending_ids = []
    for review in state.reviews:
        marker = review_marker_data(review.get("body"))
        review_state = str(review.get("state", "")).upper()
        author = nested_string(review, "user", "login")
        if is_supported_marker(marker):
            owned_reviews.append(
                {
                    "id": review.get("id"),
                    "state": review_state,
                    "author": author,
                    "marker_version": marker["version"],
                    "base_sha": marker["base"],
                    "head_sha": marker["head"],
                    "run_id": marker["run"],
                    "url": review.get("html_url"),
                }
            )
        elif review_state == "PENDING" and author == state.current_login:
            human_pending_ids.append(review.get("id"))
    owned_comments = []
    for comment in state.comments:
        marker = finding_marker_data(comment.get("body"))
        if is_supported_marker(marker):
            owned_comments.append(
                {
                    "id": comment.get("id"),
                    "review_id": comment.get("pull_request_review_id"),
                    "finding_id": marker["finding"],
                    "marker_version": marker["version"],
                    "base_sha": marker["base"],
                    "head_sha": marker["head"],
                    "run_id": marker["run"],
                    "path": comment.get("path"),
                    "line": comment.get("line"),
                    "side": comment.get("side"),
                    "url": comment.get("html_url"),
                }
            )
    return {
        "status": "audit",
        "pr": ref.url,
        "host": ref.host,
        "repository": ref.repository,
        "number": ref.number,
        "state": state.pull.get("state"),
        "draft": bool(state.pull.get("draft")),
        "base_sha": state.base_sha,
        "head_sha": state.head_sha,
        "changed_files": state.pull.get("changed_files"),
        "authenticated_user": state.current_login,
        "owned_reviews": owned_reviews,
        "owned_findings": owned_comments,
        "human_pending_review_ids": human_pending_ids,
    }


def validate_anchors(plan: ReviewPlan, files: Iterable[Mapping[str, Any]]) -> None:
    anchors_by_path: dict[str, set[tuple[int, str]]] = {}
    missing_patch_paths: set[str] = set()
    for file_value in files:
        filename = file_value.get("filename")
        if not isinstance(filename, str):
            continue
        patch = file_value.get("patch")
        if not isinstance(patch, str):
            missing_patch_paths.add(filename)
            anchors_by_path[filename] = set()
        else:
            anchors_by_path[filename] = changed_anchors(patch)
    for comment in plan.comments:
        if comment.path not in anchors_by_path:
            raise SafetyError(
                f"inline path is not in the current PR diff: {comment.path}"
            )
        if comment.path in missing_patch_paths:
            raise SafetyError(
                f"GitHub omitted the patch needed to validate anchor {comment.path}:{comment.line}"
            )
        if (comment.line, comment.side) not in anchors_by_path[comment.path]:
            raise SafetyError(
                f"anchor is not an exact changed line in the current diff: "
                f"{comment.path}:{comment.line}:{comment.side}"
            )


def same_run(marker: Mapping[str, str], plan: ReviewPlan) -> bool:
    return (
        marker.get("version") == str(SCHEMA_VERSION)
        and marker.get("base") == plan.base_sha
        and marker.get("head") == plan.head_sha
        and marker.get("run") == plan.run_id
    )


def preflight(client: GitHubClient, ref: PullRequestRef, plan: ReviewPlan) -> Preflight:
    state = fetch_state(client, ref, include_files=True)
    if str(state.pull.get("state", "")).lower() != "open":
        raise SafetyError("the PR is not open")
    if state.base_sha != plan.base_sha or state.head_sha != plan.head_sha:
        raise SafetyError(
            "the frozen base/head no longer matches the PR; discard the plan and review again"
        )
    validate_anchors(plan, state.files)

    same_snapshot_submitted = []
    pending_candidates = []
    for review in state.reviews:
        marker = review_marker_data(review.get("body"))
        if (
            not is_supported_marker(marker)
            or marker.get("base") != plan.base_sha
            or marker.get("head") != plan.head_sha
        ):
            continue
        review_state = str(review.get("state", "")).upper()
        if review_state == "PENDING":
            pending_candidates.append((review, marker))
        else:
            same_snapshot_submitted.append(review)
    if len(same_snapshot_submitted) > 1:
        review_ids = ", ".join(
            str(review.get("id")) for review in same_snapshot_submitted
        )
        raise SafetyError(
            "multiple submitted skill-owned reviews already exist for this "
            f"base/head snapshot: {review_ids}"
        )
    if same_snapshot_submitted:
        review = same_snapshot_submitted[0]
        return Preflight(
            "noop-existing-snapshot",
            state,
            integer_id(review, "existing review"),
            review.get("html_url") if isinstance(review.get("html_url"), str) else None,
        )

    resume_id: int | None = None
    for review, marker in pending_candidates:
        author = nested_string(review, "user", "login")
        review_id = integer_id(review, "pending review")
        if author == state.current_login and same_run(marker, plan):
            if resume_id is not None:
                raise SafetyError("multiple matching skill-owned pending reviews exist")
            resume_id = review_id
        else:
            raise SafetyError(
                "a different skill-owned pending review exists for this "
                f"base/head snapshot: {review_id}"
            )

    for review in state.reviews:
        if str(review.get("state", "")).upper() != "PENDING":
            continue
        if nested_string(review, "user", "login") != state.current_login:
            continue
        review_id = integer_id(review, "pending review")
        marker = review_marker_data(review.get("body"))
        if resume_id == review_id:
            continue
        if is_supported_marker(marker):
            raise SafetyError(
                f"another skill-owned pending review exists for the authenticated user: {review_id}"
            )
        raise SafetyError(
            f"a human pending review exists for the authenticated user: {review_id}"
        )

    planned_ids = {comment.finding_id for comment in plan.comments}
    planned_bodies = {comment.body for comment in plan.comments}
    for remote_comment in state.comments:
        remote_review_id = remote_comment.get("pull_request_review_id")
        marker = finding_marker_data(remote_comment.get("body"))
        plain_body = without_marker(remote_comment.get("body"), FINDING_MARKER_RE)
        if is_supported_marker(marker) and marker.get("finding") in planned_ids:
            if resume_id == remote_review_id and same_run(marker, plan):
                continue
            raise SafetyError(
                f"finding_id already exists in review history: {marker.get('finding')}"
            )
        if plain_body in planned_bodies:
            if (
                resume_id == remote_review_id
                and is_supported_marker(marker)
                and same_run(marker, plan)
            ):
                continue
            raise SafetyError("an existing inline comment has the same normalized body")

    if resume_id is not None:
        verify_review(
            client, ref, plan, resume_id, expected_state="PENDING", check_head=True
        )
        return Preflight("resume-ready", state, resume_id)
    return Preflight("valid", state)


def expected_comment_payload(
    plan: ReviewPlan, comment: CommentPlan
) -> Mapping[str, Any]:
    return {
        "path": comment.path,
        "line": comment.line,
        "side": comment.side,
        "body": comment.rendered_body(plan),
    }


def create_payload(plan: ReviewPlan) -> Mapping[str, Any]:
    return {
        "commit_id": plan.head_sha,
        "body": plan.rendered_summary(),
        "comments": [
            expected_comment_payload(plan, comment) for comment in plan.comments
        ],
    }


def rendered_comment_location(comment: Mapping[str, Any]) -> str:
    """Return only non-content fields needed to diagnose an anchor mismatch."""
    fields = (
        "line",
        "original_line",
        "side",
        "start_line",
        "original_start_line",
        "start_side",
        "position",
        "original_position",
        "commit_id",
        "original_commit_id",
    )
    observed = {field: comment.get(field) for field in fields}
    return json.dumps(observed, sort_keys=True, separators=(",", ":"))


def verify_comment_anchor(
    plan: ReviewPlan,
    expected: CommentPlan,
    remote_comment: Mapping[str, Any],
    legacy_files: Sequence[Mapping[str, Any]] | None,
) -> None:
    finding_id = expected.finding_id
    observed_line = remote_comment.get("line")
    observed_side = remote_comment.get("side")
    if observed_line is not None or observed_side is not None:
        if (
            observed_line == expected.line
            and str(observed_side or "").upper() == expected.side
        ):
            return
        raise VerificationError(
            f"finding {finding_id} anchor differs from the plan: "
            f"expected line={expected.line}, side={expected.side}; "
            f"observed {rendered_comment_location(remote_comment)}"
        )

    original_commit_id = remote_comment.get("original_commit_id")
    original_position = remote_comment.get("original_position")
    if original_commit_id is None and original_position is None:
        original_commit_id = remote_comment.get("commit_id")
        original_position = remote_comment.get("position")
    if original_commit_id != plan.head_sha or not isinstance(
        original_position, int
    ):
        raise VerificationError(
            f"finding {finding_id} has no verifiable line or legacy position: "
            f"expected line={expected.line}, side={expected.side}; "
            f"observed {rendered_comment_location(remote_comment)}"
        )

    if legacy_files is None:
        raise VerificationError(
            f"finding {finding_id} requires legacy position verification but no patches were loaded"
        )
    matching_files = [
        file_value
        for file_value in legacy_files
        if file_value.get("filename") == expected.path
    ]
    if len(matching_files) != 1 or not isinstance(
        matching_files[0].get("patch"), str
    ):
        raise VerificationError(
            f"finding {finding_id} legacy position cannot be checked against one complete patch"
        )
    expected_position = legacy_position_for_anchor(
        matching_files[0]["patch"], expected.line, expected.side
    )
    if expected_position is None or original_position != expected_position:
        raise VerificationError(
            f"finding {finding_id} legacy position differs from the frozen anchor: "
            f"expected line={expected.line}, side={expected.side}, "
            f"position={expected_position}; "
            f"observed {rendered_comment_location(remote_comment)}"
        )


def verify_review(
    client: GitHubClient,
    ref: PullRequestRef,
    plan: ReviewPlan,
    review_id: int,
    *,
    expected_state: str,
    check_head: bool,
) -> Mapping[str, Any]:
    review = client.get(f"{ref.endpoint}/reviews/{review_id}")
    comments = client.paginate(f"{ref.endpoint}/reviews/{review_id}/comments")
    if not isinstance(review, Mapping):
        raise VerificationError(f"review {review_id} returned malformed metadata")
    observed_state = str(review.get("state", "")).upper()
    if observed_state != expected_state:
        raise VerificationError(
            f"review {review_id} state is {observed_state or 'missing'}, expected {expected_state}"
        )
    if review.get("commit_id") != plan.head_sha:
        raise VerificationError(f"review {review_id} is not bound to the planned head")
    marker = review_marker_data(review.get("body"))
    if not marker or not same_run(marker, plan):
        raise VerificationError(
            f"review {review_id} does not have the expected ownership marker"
        )
    if without_marker(review.get("body"), REVIEW_MARKER_RE) != plan.summary_body():
        raise VerificationError(f"review {review_id} summary differs from the plan")
    if len(comments) != len(plan.comments):
        raise VerificationError(
            f"review {review_id} has {len(comments)} comments, expected {len(plan.comments)}"
        )
    expected_by_id = {comment.finding_id: comment for comment in plan.comments}
    observed_ids: set[str] = set()
    legacy_files: list[Mapping[str, Any]] | None = None
    if any(
        remote_comment.get("line") is None
        and remote_comment.get("side") is None
        for remote_comment in comments
    ):
        legacy_files = client.paginate(f"{ref.endpoint}/files")
    for remote_comment in comments:
        marker = finding_marker_data(remote_comment.get("body"))
        if not marker or not same_run(marker, plan):
            raise VerificationError(
                f"review {review_id} contains a non-owned inline comment"
            )
        finding_id = marker.get("finding", "")
        expected = expected_by_id.get(finding_id)
        if expected is None or finding_id in observed_ids:
            raise VerificationError(
                f"review {review_id} has an unexpected finding marker"
            )
        observed_ids.add(finding_id)
        if remote_comment.get("path") != expected.path:
            raise VerificationError(f"finding {finding_id} path differs from the plan")
        verify_comment_anchor(plan, expected, remote_comment, legacy_files)
        if (
            without_marker(remote_comment.get("body"), FINDING_MARKER_RE)
            != expected.body
        ):
            raise VerificationError(f"finding {finding_id} body differs from the plan")
    if observed_ids != set(expected_by_id):
        raise VerificationError(f"review {review_id} is missing planned findings")
    if check_head:
        current = client.get(ref.endpoint)
        if not isinstance(current, Mapping):
            raise VerificationError("current PR metadata is malformed")
        if (
            nested_string(current, "base", "sha") != plan.base_sha
            or nested_string(current, "head", "sha") != plan.head_sha
        ):
            raise VerificationError(
                "the PR base or head changed during the pending transaction"
            )
    return review


def pending_is_exclusively_owned(
    client: GitHubClient,
    ref: PullRequestRef,
    plan: ReviewPlan,
    review_id: int,
) -> bool:
    try:
        review = client.get(f"{ref.endpoint}/reviews/{review_id}")
        comments = client.paginate(f"{ref.endpoint}/reviews/{review_id}/comments")
        login = authenticated_login(client)
    except TransactionError:
        return False
    if (
        not isinstance(review, Mapping)
        or str(review.get("state", "")).upper() != "PENDING"
    ):
        return False
    if nested_string(review, "user", "login") != login:
        return False
    marker = review_marker_data(review.get("body"))
    if not marker or not same_run(marker, plan):
        return False
    for comment in comments:
        finding = finding_marker_data(comment.get("body"))
        if not finding or not same_run(finding, plan):
            return False
    return True


def delete_owned_pending(
    client: GitHubClient,
    ref: PullRequestRef,
    plan: ReviewPlan,
    review_id: int,
) -> None:
    if not pending_is_exclusively_owned(client, ref, plan, review_id):
        raise VerificationError(
            f"pending review {review_id} could not be proven exclusively skill-owned; it was not deleted"
        )
    client.delete(f"{ref.endpoint}/reviews/{review_id}")
    reviews = client.paginate(f"{ref.endpoint}/reviews")
    for review in reviews:
        if (
            review.get("id") == review_id
            and str(review.get("state", "")).upper() == "PENDING"
        ):
            raise VerificationError(
                f"pending review {review_id} still exists after deletion"
            )


def reconcile_created_review(
    client: GitHubClient, ref: PullRequestRef, plan: ReviewPlan
) -> tuple[str, int, Mapping[str, Any]] | None:
    login = authenticated_login(client)
    reviews = client.paginate(f"{ref.endpoint}/reviews")
    matches = []
    for review in reviews:
        marker = review_marker_data(review.get("body"))
        if (
            marker
            and same_run(marker, plan)
            and nested_string(review, "user", "login") == login
        ):
            matches.append(review)
    if len(matches) != 1:
        return None
    review = matches[0]
    review_id = integer_id(review, "reconciled review")
    return str(review.get("state", "")).upper(), review_id, review


def publish(
    client: GitHubClient,
    ref: PullRequestRef,
    plan: ReviewPlan,
    event: str,
) -> Mapping[str, Any]:
    event = event.upper()
    if event not in EVENT_STATES:
        raise PlanError(f"unsupported review event: {event}")
    blocking = sum(comment.disposition == "blocking" for comment in plan.comments)
    if event == "REQUEST_CHANGES" and blocking == 0:
        raise PlanError("REQUEST_CHANGES requires at least one blocking finding")
    if event == "APPROVE" and blocking:
        raise PlanError("APPROVE cannot be used with a blocking finding")

    checked = preflight(client, ref, plan)
    if checked.status == "noop-existing-snapshot":
        existing_comments = sum(
            comment.get("pull_request_review_id") == checked.review_id
            for comment in checked.state.comments
        )
        existing_review = next(
            review
            for review in checked.state.reviews
            if review.get("id") == checked.review_id
        )
        return {
            "status": checked.status,
            "pr": ref.url,
            "base_sha": plan.base_sha,
            "head_sha": plan.head_sha,
            "review_id": checked.review_id,
            "review_url": checked.review_url,
            "observed_state": str(existing_review.get("state", "")).upper(),
            "inline_count": existing_comments,
        }

    review_id = checked.review_id
    if review_id is None:
        try:
            created = client.post(f"{ref.endpoint}/reviews", create_payload(plan))
            if not isinstance(created, Mapping):
                raise VerificationError("create review returned malformed metadata")
            review_id = integer_id(created, "created review")
        except TransactionError as error:
            reconciled = reconcile_created_review(client, ref, plan)
            if reconciled is None:
                raise GitHubError(
                    f"review creation failed and reconciliation did not prove one owned review; "
                    f"no retry was attempted. {error}",
                    ambiguous_write=True,
                ) from error
            observed_state, review_id, review = reconciled
            if observed_state in FINAL_STATES:
                expected_state = EVENT_STATES[event]
                verify_review(
                    client,
                    ref,
                    plan,
                    review_id,
                    expected_state=expected_state,
                    check_head=False,
                )
                return publication_result(
                    "published-reconciled", ref, plan, event, review_id, review
                )
            if observed_state != "PENDING":
                raise VerificationError(
                    f"reconciled review {review_id} has unexpected state {observed_state}"
                ) from error

    try:
        verify_review(
            client,
            ref,
            plan,
            review_id,
            expected_state="PENDING",
            check_head=True,
        )
    except TransactionError:
        delete_owned_pending(client, ref, plan, review_id)
        raise

    submit_payload = {"body": plan.rendered_summary(), "event": event}
    submit_endpoint = f"{ref.endpoint}/reviews/{review_id}/events"
    try:
        client.post(submit_endpoint, submit_payload)
    except GitHubError as error:
        try:
            review = verify_review(
                client,
                ref,
                plan,
                review_id,
                expected_state=EVENT_STATES[event],
                check_head=False,
            )
        except TransactionError as reconciliation_error:
            if pending_is_exclusively_owned(client, ref, plan, review_id):
                delete_owned_pending(client, ref, plan, review_id)
            raise GitHubError(
                f"review submission failed and final state was not proven; no retry was attempted. "
                f"{error}; reconciliation: {reconciliation_error}",
                ambiguous_write=True,
            ) from error
        return publication_result(
            "published-reconciled", ref, plan, event, review_id, review
        )

    review = verify_review(
        client,
        ref,
        plan,
        review_id,
        expected_state=EVENT_STATES[event],
        check_head=False,
    )
    return publication_result("published", ref, plan, event, review_id, review)


def publication_result(
    status: str,
    ref: PullRequestRef,
    plan: ReviewPlan,
    event: str,
    review_id: int,
    review: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "status": status,
        "pr": ref.url,
        "base_sha": plan.base_sha,
        "head_sha": plan.head_sha,
        "profile": plan.profile,
        "event": event,
        "review_id": review_id,
        "review_url": review.get("html_url"),
        "inline_count": len(plan.comments),
        "run_id": plan.run_id,
    }


def rendered_existing_finding_marker(marker: Mapping[str, str]) -> str:
    return (
        f"<!-- gh-review-pr:finding v={marker['version']} base={marker['base']} "
        f"head={marker['head']} run={marker['run']} id={marker['finding']} -->"
    )


def locate_owned_finding(
    state: RemoteState,
    *,
    base_sha: str,
    head_sha: str,
    review_id: int,
    finding_id: str,
    operation: str,
) -> tuple[Mapping[str, Any], Mapping[str, str]]:
    matching_reviews = [
        review
        for review in state.reviews
        if review.get("id") == review_id
    ]
    if len(matching_reviews) != 1:
        raise SafetyError(
            f"the {operation} review_id does not identify one current review"
        )
    review = matching_reviews[0]
    owned_review_marker = review_marker_data(review.get("body"))
    if (
        not is_supported_marker(owned_review_marker)
        or owned_review_marker.get("base") != base_sha
        or owned_review_marker.get("head") != head_sha
        or nested_string(review, "user", "login") != state.current_login
        or str(review.get("state", "")).upper() not in FINAL_STATES
    ):
        raise SafetyError("the target review is not a submitted skill-owned review")
    matching_comments = []
    for comment in state.comments:
        marker = finding_marker_data(comment.get("body"))
        if (
            marker
            and comment.get("pull_request_review_id") == review_id
            and marker.get("finding") == finding_id
        ):
            matching_comments.append((comment, marker))
    if len(matching_comments) != 1:
        raise SafetyError("the finding_id does not identify one comment in the review")
    comment, marker = matching_comments[0]
    if (
        not is_supported_marker(marker)
        or marker.get("version") != owned_review_marker.get("version")
        or marker.get("base") != base_sha
        or marker.get("head") != head_sha
        or marker.get("run") != owned_review_marker.get("run")
        or nested_string(comment, "user", "login") != state.current_login
    ):
        raise SafetyError("the target comment is not exclusively skill-owned")
    return comment, marker


def current_pr_pair(client: GitHubClient, ref: PullRequestRef) -> tuple[str, str]:
    pull = client.get(ref.endpoint)
    if not isinstance(pull, Mapping):
        raise GitHubError("GitHub returned malformed PR metadata")
    base_sha = nested_string(pull, "base", "sha")
    head_sha = nested_string(pull, "head", "sha")
    if not SHA_RE.fullmatch(base_sha) or not SHA_RE.fullmatch(head_sha):
        raise GitHubError("GitHub returned missing or non-full base/head SHAs")
    return base_sha, head_sha


def verify_amendment_target(
    client: GitHubClient,
    ref: PullRequestRef,
    amendment: AmendmentPlan,
) -> tuple[int, Mapping[str, str], str]:
    state = fetch_state(client, ref, include_files=False)
    if state.base_sha != amendment.base_sha or state.head_sha != amendment.head_sha:
        raise SafetyError(
            "the frozen base/head no longer matches the PR; discard the amendment"
        )
    comment, marker = locate_owned_finding(
        state,
        base_sha=amendment.base_sha,
        head_sha=amendment.head_sha,
        review_id=amendment.review_id,
        finding_id=amendment.finding_id,
        operation="amendment",
    )
    existing_classification = issue_classification(comment.get("body"))
    replacement_classification = issue_classification(amendment.body)
    if existing_classification is None:
        raise SafetyError("the target finding classification could not be verified")
    if replacement_classification != existing_classification:
        raise SafetyError(
            "an amendment may change wording only; disposition, severity, and category "
            "must match the submitted finding"
        )
    comment_id = integer_id(comment, "amendment comment")
    rendered_body = (
        f"{amendment.body}\n\n{rendered_existing_finding_marker(marker)}"
    )
    return comment_id, marker, rendered_body


def verify_reply_target(
    client: GitHubClient,
    ref: PullRequestRef,
    reply: ReplyPlan,
) -> tuple[int, str, str, str]:
    state = fetch_state(client, ref, include_files=False)
    comment, _marker = locate_owned_finding(
        state,
        base_sha=reply.base_sha,
        head_sha=reply.head_sha,
        review_id=reply.review_id,
        finding_id=reply.finding_id,
        operation="reply",
    )
    return (
        integer_id(comment, "reply target comment"),
        state.current_login,
        state.base_sha,
        state.head_sha,
    )


def verify_amended_comment(
    client: GitHubClient,
    ref: PullRequestRef,
    amendment: AmendmentPlan,
    comment_id: int,
    expected_body: str,
) -> Mapping[str, Any]:
    comment = client.get(
        f"repos/{ref.owner}/{ref.repo}/pulls/comments/{comment_id}"
    )
    if not isinstance(comment, Mapping):
        raise VerificationError("amended comment returned malformed metadata")
    marker = finding_marker_data(comment.get("body"))
    if (
        comment.get("id") != comment_id
        or comment.get("pull_request_review_id") != amendment.review_id
        or not is_supported_marker(marker)
        or marker.get("base") != amendment.base_sha
        or marker.get("head") != amendment.head_sha
        or marker.get("finding") != amendment.finding_id
        or comment.get("body") != expected_body
        or nested_string(comment, "user", "login") != authenticated_login(client)
    ):
        raise VerificationError(
            "amended comment did not match the requested owned finding"
        )
    return comment


def amend_comment(
    client: GitHubClient,
    ref: PullRequestRef,
    amendment: AmendmentPlan,
) -> Mapping[str, Any]:
    comment_id, _marker, rendered_body = verify_amendment_target(
        client, ref, amendment
    )
    current_base_sha, current_head_sha = current_pr_pair(client, ref)
    if (
        current_base_sha != amendment.base_sha
        or current_head_sha != amendment.head_sha
    ):
        raise SafetyError(
            "the PR base/head changed while preparing the amendment; discard it"
        )
    endpoint = f"repos/{ref.owner}/{ref.repo}/pulls/comments/{comment_id}"
    status = "amended"
    try:
        client.patch(endpoint, {"body": rendered_body})
    except GitHubError as error:
        try:
            comment = verify_amended_comment(
                client, ref, amendment, comment_id, rendered_body
            )
        except TransactionError as reconciliation_error:
            raise GitHubError(
                "comment amendment failed and the requested body was not proven; "
                f"no retry was attempted. {error}; reconciliation: {reconciliation_error}",
                ambiguous_write=True,
            ) from error
        status = "amended-reconciled"
    else:
        comment = verify_amended_comment(
            client, ref, amendment, comment_id, rendered_body
        )
    return {
        "status": status,
        "pr": ref.url,
        "base_sha": amendment.base_sha,
        "head_sha": amendment.head_sha,
        "review_id": amendment.review_id,
        "comment_id": comment_id,
        "finding_id": amendment.finding_id,
        "comment_url": comment.get("html_url"),
    }


def find_matching_replies(
    comments: Iterable[Mapping[str, Any]],
    target_comment_id: int,
    body: str,
    login: str,
) -> list[Mapping[str, Any]]:
    return [
        comment
        for comment in comments
        if comment.get("in_reply_to_id") == target_comment_id
        and comment.get("body") == body
        and nested_string(comment, "user", "login") == login
    ]


def verify_owned_reply(
    client: GitHubClient,
    ref: PullRequestRef,
    target_comment_id: int,
    body: str,
    comment_id: int,
) -> Mapping[str, Any]:
    comment = client.get(
        f"repos/{ref.owner}/{ref.repo}/pulls/comments/{comment_id}"
    )
    if (
        not isinstance(comment, Mapping)
        or comment.get("id") != comment_id
        or comment.get("in_reply_to_id") != target_comment_id
        or comment.get("body") != body
        or nested_string(comment, "user", "login") != authenticated_login(client)
    ):
        raise VerificationError(
            "reply did not match the requested owned finding response"
        )
    return comment


def owned_reply_result(
    status: str,
    ref: PullRequestRef,
    reply: ReplyPlan,
    target_comment_id: int,
    reply_comment_id: int,
    comment: Mapping[str, Any],
    current_base_sha: str,
    current_head_sha: str,
) -> Mapping[str, Any]:
    return {
        "status": status,
        "pr": ref.url,
        "base_sha": reply.base_sha,
        "head_sha": reply.head_sha,
        "review_base_sha": reply.base_sha,
        "review_head_sha": reply.head_sha,
        "current_base_sha": current_base_sha,
        "current_head_sha": current_head_sha,
        "review_id": reply.review_id,
        "target_comment_id": target_comment_id,
        "reply_comment_id": reply_comment_id,
        "finding_id": reply.finding_id,
        "comment_url": comment.get("html_url"),
    }


def reply_to_owned_finding(
    client: GitHubClient,
    ref: PullRequestRef,
    reply: ReplyPlan,
) -> Mapping[str, Any]:
    (
        target_comment_id,
        login,
        initial_current_base_sha,
        initial_current_head_sha,
    ) = verify_reply_target(client, ref, reply)
    existing = find_matching_replies(
        client.paginate(f"{ref.endpoint}/comments"),
        target_comment_id,
        reply.body,
        login,
    )
    if len(existing) > 1:
        raise SafetyError("multiple identical owned replies already exist")
    if existing:
        comment = existing[0]
        current_base_sha, current_head_sha = current_pr_pair(client, ref)
        return owned_reply_result(
            "noop-existing-reply",
            ref,
            reply,
            target_comment_id,
            integer_id(comment, "existing reply"),
            comment,
            current_base_sha,
            current_head_sha,
        )

    current_base_sha, current_head_sha = current_pr_pair(client, ref)
    if (
        current_base_sha != initial_current_base_sha
        or current_head_sha != initial_current_head_sha
    ):
        raise SafetyError(
            "the PR base/head changed while preparing the reply; re-run against the "
            "same owned finding"
        )

    endpoint = f"{ref.endpoint}/comments/{target_comment_id}/replies"
    status = "replied"
    try:
        created = client.post(endpoint, {"body": reply.body})
        if not isinstance(created, Mapping):
            raise VerificationError("create reply returned malformed metadata")
        reply_comment_id = integer_id(created, "created reply")
    except TransactionError as error:
        matches = find_matching_replies(
            client.paginate(f"{ref.endpoint}/comments"),
            target_comment_id,
            reply.body,
            login,
        )
        if len(matches) != 1:
            raise GitHubError(
                "reply creation failed and one exact response was not proven; "
                f"no retry was attempted. {error}",
                ambiguous_write=True,
            ) from error
        reply_comment_id = integer_id(matches[0], "reconciled reply")
        status = "replied-reconciled"
    comment = verify_owned_reply(
        client, ref, target_comment_id, reply.body, reply_comment_id
    )
    return owned_reply_result(
        status,
        ref,
        reply,
        target_comment_id,
        reply_comment_id,
        comment,
        current_base_sha,
        current_head_sha,
    )


def validation_result(
    ref: PullRequestRef, plan: ReviewPlan, result: Preflight
) -> Mapping[str, Any]:
    existing_inline_count = None
    if result.status == "noop-existing-snapshot":
        existing_inline_count = sum(
            comment.get("pull_request_review_id") == result.review_id
            for comment in result.state.comments
        )
    return {
        "status": result.status,
        "pr": ref.url,
        "base_sha": plan.base_sha,
        "head_sha": plan.head_sha,
        "run_id": plan.run_id,
        "planned_inline_count": len(plan.comments),
        "existing_inline_count": existing_inline_count,
        "review_id": result.review_id,
        "review_url": result.review_url,
    }


def parser() -> argparse.ArgumentParser:
    root = JsonArgumentParser(
        description="Audit, validate, publish, amend, or reply to a gh-review-pr review"
    )
    subparsers = root.add_subparsers(dest="command", required=True)
    for name in ("audit", "validate", "publish", "amend", "reply"):
        command = subparsers.add_parser(name)
        command.add_argument("--pr", required=True, help="full GitHub pull request URL")
        command.add_argument(
            "--timeout", type=int, default=60, help="per-request timeout in seconds"
        )
        if name in {"validate", "publish"}:
            command.add_argument(
                "--plan", required=True, type=Path, help="review plan JSON"
            )
        if name == "amend":
            command.add_argument(
                "--amendment",
                required=True,
                type=Path,
                help="owned finding amendment JSON",
            )
        if name == "reply":
            command.add_argument(
                "--reply",
                required=True,
                type=Path,
                help="owned finding reply JSON",
            )
        if name == "publish":
            command.add_argument(
                "--event",
                choices=tuple(EVENT_STATES),
                default="COMMENT",
                help="final review event; decision events require explicit user intent",
            )
    return root


def emit(value: Mapping[str, Any], *, stream: Any = sys.stdout) -> None:
    json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write("\n")


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if args.timeout < 1 or args.timeout > 600:
            raise PlanError("timeout must be between 1 and 600 seconds")
        ref = PullRequestRef.parse(args.pr)
        client = GitHubClient(ref.host, timeout=args.timeout)
        if args.command == "audit":
            result = audit_result(ref, fetch_state(client, ref, include_files=False))
        elif args.command == "amend":
            result = amend_comment(client, ref, load_amendment(args.amendment))
        elif args.command == "reply":
            result = reply_to_owned_finding(client, ref, load_reply(args.reply))
        else:
            plan = load_plan(args.plan)
            if args.command == "validate":
                result = validation_result(ref, plan, preflight(client, ref, plan))
            else:
                result = publish(client, ref, plan, args.event)
        emit(result)
        return 0
    except TransactionError as error:
        emit(
            {"status": "error", "error": error.code, "message": str(error)},
            stream=sys.stderr,
        )
        return error.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
