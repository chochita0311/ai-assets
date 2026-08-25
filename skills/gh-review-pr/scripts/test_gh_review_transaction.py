#!/usr/bin/env python3
"""Offline regression tests for gh_review_transaction.py."""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from collections.abc import Mapping
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from typing import Any

import gh_review_transaction as transaction

BASE_SHA = "a" * 40
HEAD_SHA = "b" * 40
NEW_HEAD_SHA = "c" * 40
PR_URL = "https://github.example.com/octo/widgets/pull/17"
PATCH = """@@ -1,2 +1,3 @@
 existing
+replacement
 retained
"""
MULTI_HUNK_PATCH = """@@ -3,6 +3,7 @@
 context 1
 context 2
 context 3
+addition 1
 context 4
 context 5
 context 6
@@ -14,8 +15,8 @@
 context 7
 context 8
 context 9
-deletion 1
 context 10
+addition 2
 context 11
 context 12
 context 13
@@ -53,7 +54,9 @@
 context 14
 context 15
 context 16
-deletion 2
+addition 3
+addition 4
+target
 context 17
 context 18
 context 19
"""


def make_summary(
    *,
    scope: str = "One human-authored changed file was reviewed end to end.",
    focus: tuple[str, ...] = ("failure atomicity", "recovery behavior"),
    evidence: tuple[transaction.ReviewEvidence, ...] | None = None,
    coverage_gaps: tuple[str, ...] = (),
    notes: tuple[transaction.ReviewNote, ...] = (),
) -> transaction.ReviewSummary:
    return transaction.ReviewSummary(
        overview=(
            "This PR replaces stored state and the review focused on failure "
            "atomicity and recovery behavior."
        ),
        scope=scope,
        focus=focus,
        evidence=evidence
        or (
            transaction.ReviewEvidence(
                "boundary-behavior",
                "Compared the changed replacement boundary against the base behavior.",
            ),
            transaction.ReviewEvidence(
                "integration-consumers",
                "Traced the updated state through its durable consumer.",
            ),
            transaction.ReviewEvidence(
                "tests-validation",
                "Checked the failure-path test and adversarial recovery case.",
            ),
        ),
        coverage_gaps=coverage_gaps,
        review_notes=notes,
    )


def make_plan(
    *,
    line: int = 2,
    comments: bool = True,
    profile: str = "balanced",
    summary: transaction.ReviewSummary | None = None,
) -> transaction.ReviewPlan:
    findings: tuple[transaction.CommentPlan, ...]
    if comments:
        findings = (
            transaction.CommentPlan(
                finding_id="preserve-existing-state",
                path="src/state.py",
                line=line,
                side="RIGHT",
                severity="high",
                confidence="high",
                disposition="blocking",
                category="data-integrity",
                body=(
                    "issue (blocking, high, data-integrity): Preserve existing state on failure\n\n"
                    "The replacement path deletes the durable value first. Store the new value "
                    "before removing the old one."
                ),
            ),
        )
    else:
        findings = ()
    return transaction.ReviewPlan(
        base_sha=BASE_SHA,
        head_sha=HEAD_SHA,
        profile=profile,
        summary=summary or make_summary(),
        comments=findings,
    )


def plan_payload(plan: transaction.ReviewPlan) -> dict[str, Any]:
    return {
        "schema_version": transaction.SCHEMA_VERSION,
        "base_sha": plan.base_sha,
        "head_sha": plan.head_sha,
        "profile": plan.profile,
        "summary": plan.summary.as_dict(),
        "comments": [comment.__dict__ for comment in plan.comments],
    }


def make_amendment(
    review_id: int, *, body: str | None = None
) -> transaction.AmendmentPlan:
    return transaction.AmendmentPlan(
        base_sha=BASE_SHA,
        head_sha=HEAD_SHA,
        review_id=review_id,
        finding_id="preserve-existing-state",
        body=body
        or (
            "issue (blocking, high, data-integrity): Clarify the failure path\n\n"
            "The changed exception propagation makes the failure reachable. "
            "Close the application context when initialization fails."
        ),
    )


def make_reply(review_id: int, *, body: str | None = None) -> transaction.ReplyPlan:
    return transaction.ReplyPlan(
        base_sha=BASE_SHA,
        head_sha=HEAD_SHA,
        review_id=review_id,
        finding_id="preserve-existing-state",
        body=body or "Applied the bounded startup fix.",
    )


class FakeGitHubClient:
    def __init__(self) -> None:
        self.base_sha = BASE_SHA
        self.head_sha = HEAD_SHA
        self.login = "review-bot"
        self.files: list[Mapping[str, Any]] = [
            {"filename": "src/state.py", "patch": PATCH, "status": "modified"}
        ]
        self.reviews: list[dict[str, Any]] = []
        self.comments: list[dict[str, Any]] = []
        self.next_review_id = 101
        self.next_comment_id = 501
        self.post_calls: list[str] = []
        self.patch_calls: list[str] = []
        self.delete_calls: list[str] = []
        self.create_failure: str | None = None
        self.submit_failure_after_apply = False
        self.head_after_create: str | None = None
        self.created_comment_overrides: dict[str, Any] = {}
        self.patch_failure_after_apply = False
        self.reply_failure_after_apply = False
        self.head_after_comment_list: str | None = None

    @staticmethod
    def pull_endpoint() -> str:
        return "repos/octo/widgets/pulls/17"

    def pull(self) -> Mapping[str, Any]:
        return {
            "state": "open",
            "draft": False,
            "changed_files": len(self.files),
            "base": {"sha": self.base_sha},
            "head": {"sha": self.head_sha},
        }

    def get(self, endpoint: str) -> Any:
        if endpoint == "user":
            return {"login": self.login}
        if endpoint == self.pull_endpoint():
            return self.pull()
        comment_prefix = "repos/octo/widgets/pulls/comments/"
        if endpoint.startswith(comment_prefix) and endpoint[len(comment_prefix) :].isdigit():
            comment_id = int(endpoint[len(comment_prefix) :])
            for comment in self.comments:
                if comment["id"] == comment_id:
                    return dict(comment)
            raise transaction.GitHubError(f"comment {comment_id} not found")
        prefix = f"{self.pull_endpoint()}/reviews/"
        if endpoint.startswith(prefix) and endpoint[len(prefix) :].isdigit():
            review_id = int(endpoint[len(prefix) :])
            for review in self.reviews:
                if review["id"] == review_id:
                    return dict(review)
            raise transaction.GitHubError(f"review {review_id} not found")
        raise AssertionError(f"unexpected GET endpoint: {endpoint}")

    def paginate(self, endpoint: str) -> list[Mapping[str, Any]]:
        if endpoint == f"{self.pull_endpoint()}/files":
            return [dict(value) for value in self.files]
        review_comment_prefix = f"{self.pull_endpoint()}/reviews/"
        if endpoint.startswith(review_comment_prefix) and endpoint.endswith(
            "/comments"
        ):
            review_id = int(endpoint[len(review_comment_prefix) : -len("/comments")])
            return [
                dict(value)
                for value in self.comments
                if value["pull_request_review_id"] == review_id
            ]
        if endpoint == f"{self.pull_endpoint()}/reviews":
            return [dict(value) for value in self.reviews]
        if endpoint == f"{self.pull_endpoint()}/comments":
            comments = [dict(value) for value in self.comments]
            if self.head_after_comment_list:
                self.head_sha = self.head_after_comment_list
                self.head_after_comment_list = None
            return comments
        raise AssertionError(f"unexpected paginated endpoint: {endpoint}")

    def post(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        self.post_calls.append(endpoint)
        if endpoint == f"{self.pull_endpoint()}/reviews":
            if self.create_failure == "before":
                raise transaction.GitHubError("permission denied", ambiguous_write=True)
            review = {
                "id": self.next_review_id,
                "state": "PENDING",
                "commit_id": payload["commit_id"],
                "body": payload["body"],
                "html_url": f"https://github.example.com/review/{self.next_review_id}",
                "user": {"login": self.login},
            }
            self.next_review_id += 1
            self.reviews.append(review)
            for comment_payload in payload["comments"]:
                comment = {
                    "id": self.next_comment_id,
                    "pull_request_review_id": review["id"],
                    "html_url": f"https://github.example.com/comment/{self.next_comment_id}",
                    "user": {"login": self.login},
                    **comment_payload,
                    **self.created_comment_overrides,
                }
                self.next_comment_id += 1
                self.comments.append(comment)
            if self.head_after_create:
                self.head_sha = self.head_after_create
            if self.create_failure == "after":
                raise transaction.GitHubError("connection reset", ambiguous_write=True)
            return dict(review)

        event_suffix = "/events"
        if endpoint.startswith(
            f"{self.pull_endpoint()}/reviews/"
        ) and endpoint.endswith(event_suffix):
            review_id = int(endpoint.split("/")[-2])
            review = next(value for value in self.reviews if value["id"] == review_id)
            review["state"] = transaction.EVENT_STATES[payload["event"]]
            review["body"] = payload["body"]
            if self.submit_failure_after_apply:
                raise transaction.GitHubError("connection reset", ambiguous_write=True)
            return dict(review)
        reply_suffix = "/replies"
        if endpoint.startswith(f"{self.pull_endpoint()}/comments/") and endpoint.endswith(reply_suffix):
            target_comment_id = int(endpoint.split("/")[-2])
            target = next(
                value for value in self.comments if value["id"] == target_comment_id
            )
            comment = {
                "id": self.next_comment_id,
                "pull_request_review_id": target["pull_request_review_id"],
                "in_reply_to_id": target_comment_id,
                "body": payload["body"],
                "html_url": f"https://github.example.com/comment/{self.next_comment_id}",
                "user": {"login": self.login},
            }
            self.next_comment_id += 1
            self.comments.append(comment)
            if self.reply_failure_after_apply:
                raise transaction.GitHubError("connection reset", ambiguous_write=True)
            return dict(comment)
        raise AssertionError(f"unexpected POST endpoint: {endpoint}")

    def patch(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        self.patch_calls.append(endpoint)
        comment_id = int(endpoint.split("/")[-1])
        comment = next(value for value in self.comments if value["id"] == comment_id)
        comment["body"] = payload["body"]
        if self.patch_failure_after_apply:
            raise transaction.GitHubError("connection reset", ambiguous_write=True)
        return dict(comment)

    def delete(self, endpoint: str) -> None:
        self.delete_calls.append(endpoint)
        review_id = int(endpoint.split("/")[-1])
        self.reviews = [value for value in self.reviews if value["id"] != review_id]
        self.comments = [
            value
            for value in self.comments
            if value["pull_request_review_id"] != review_id
        ]

    def add_review(self, plan: transaction.ReviewPlan, state: str = "COMMENTED") -> int:
        review_id = self.next_review_id
        self.next_review_id += 1
        self.reviews.append(
            {
                "id": review_id,
                "state": state,
                "commit_id": plan.head_sha,
                "body": plan.rendered_summary(),
                "html_url": f"https://github.example.com/review/{review_id}",
                "user": {"login": self.login},
            }
        )
        for finding in plan.comments:
            self.comments.append(
                {
                    "id": self.next_comment_id,
                    "pull_request_review_id": review_id,
                    "path": finding.path,
                    "line": finding.line,
                    "side": finding.side,
                    "body": finding.rendered_body(plan),
                    "html_url": f"https://github.example.com/comment/{self.next_comment_id}",
                    "user": {"login": self.login},
                }
            )
            self.next_comment_id += 1
        return review_id


class TransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ref = transaction.PullRequestRef.parse(PR_URL)

    def test_parse_pr_url_requires_canonical_full_url(self) -> None:
        self.assertEqual(self.ref.repository, "octo/widgets")
        with self.assertRaises(transaction.PlanError):
            transaction.PullRequestRef.parse(
                "https://github.example.com/octo/widgets/pull/17/files"
            )

    def test_cli_usage_errors_follow_the_json_error_contract(self) -> None:
        stderr = StringIO()
        with redirect_stderr(stderr):
            exit_code = transaction.main(["validate"])
        payload = json.loads(stderr.getvalue())
        self.assertEqual(exit_code, transaction.PlanError.exit_code)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["error"], "invalid-plan")

    def test_patch_parser_only_exposes_changed_side(self) -> None:
        anchors = transaction.changed_anchors(PATCH)
        self.assertIn((2, "RIGHT"), anchors)
        self.assertNotIn((2, "LEFT"), anchors)
        self.assertNotIn((1, "RIGHT"), anchors)

    def test_legacy_position_counts_later_hunk_headers(self) -> None:
        self.assertEqual(
            transaction.legacy_position_for_anchor(MULTI_HUNK_PATCH, 59, "RIGHT"),
            25,
        )

    def test_plan_loader_accepts_the_documented_schema(self) -> None:
        plan = make_plan()
        raw = plan_payload(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_plan(path)
        self.assertEqual(loaded, plan)

    def test_rendered_summary_contains_a_structured_visible_receipt(self) -> None:
        summary = make_plan(
            summary=make_summary(
                notes=(
                    transaction.ReviewNote(
                        "positive", "The source and generated contract stay aligned."
                    ),
                )
            )
        ).summary_body()
        self.assertEqual(
            summary,
            """## Review summary

This PR replaces stored state and the review focused on failure atomicity and recovery behavior.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `balanced` |
| Snapshot | `bbbbbbb` |
| Scope | One human-authored changed file was reviewed end to end. |
| Focus | failure atomicity; recovery behavior |
| Findings | **1 blocking** · 0 non-blocking · 0 questions · 0 suggestions |
| Coverage gaps | None recorded. |

### Review evidence

- **Boundary / behavior** — Compared the changed replacement boundary against the base behavior.
- **Integration / consumers** — Traced the updated state through its durable consumer.
- **Tests / validation** — Checked the failure-path test and adversarial recovery case.

### Review notes

- **Positive** — The source and generated contract stay aligned.""",
        )
        self.assertNotIn("[!WARNING]", summary)

    def test_rendered_summary_highlights_each_coverage_gap_on_its_own_line(self) -> None:
        summary = make_plan(
            comments=False,
            profile="focused",
            summary=make_summary(
                coverage_gaps=(
                    "One binary file was not reviewable.",
                    "The provider truncated one patch.",
                )
            ),
        ).summary_body()
        self.assertIn("| Coverage gaps | 2 recorded; see warning below. |", summary)
        self.assertEqual(summary.count("> [!WARNING]"), 1)
        self.assertIn(
            "> **Coverage gaps:**\n"
            ">\n"
            "> - One binary file was not reviewable.\n"
            "> - The provider truncated one patch.",
            summary,
        )
        self.assertNotIn(".;", summary)

    def test_rendered_summary_uses_a_singular_gap_label(self) -> None:
        summary = make_plan(
            comments=False,
            profile="focused",
            summary=make_summary(
                coverage_gaps=("The runtime smoke test was not available.",)
            ),
        ).summary_body()
        self.assertIn("| Coverage gaps | 1 recorded; see warning below. |", summary)
        self.assertIn(
            "> **Coverage gap:**\n"
            ">\n"
            "> - The runtime smoke test was not available.",
            summary,
        )
        self.assertNotIn("> **Coverage gaps:**", summary)

    def test_rendered_summary_escapes_table_cell_separators(self) -> None:
        plan = make_plan(
            summary=make_summary(
                scope="Reviewed src/a.py | src/b.py end to end.",
                focus=("read | write boundary",),
            )
        )
        raw = plan_payload(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "table-cell-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_plan(path)
        summary = loaded.summary_body()
        self.assertIn("Reviewed src/a.py \\| src/b.py end to end.", summary)
        self.assertIn("read \\| write boundary", summary)

    def test_reply_loader_returns_a_distinct_reply_plan(self) -> None:
        reply = make_reply(456)
        raw = {
            "schema_version": transaction.SCHEMA_VERSION,
            "base_sha": reply.base_sha,
            "head_sha": reply.head_sha,
            "review_id": reply.review_id,
            "finding_id": reply.finding_id,
            "body": reply.body,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reply.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_reply(path)
        self.assertIsInstance(loaded, transaction.ReplyPlan)
        self.assertEqual(loaded, reply)

    def test_documented_plan_example_matches_the_loader(self) -> None:
        reference = (
            Path(__file__).parent.parent / "references" / "github-publishing.md"
        ).read_text(encoding="utf-8")
        match = re.search(r"```json\n(?P<plan>.*?)\n```", reference, re.DOTALL)
        self.assertIsNotNone(match)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "documented-plan.json"
            path.write_text(match.group("plan"), encoding="utf-8")
            loaded = transaction.load_plan(path)
        self.assertEqual(loaded.base_sha, "a" * 40)
        self.assertEqual(len(loaded.comments), 1)

    def test_documented_mutation_examples_match_the_loaders(self) -> None:
        reference = (
            Path(__file__).parent.parent / "references" / "github-publishing.md"
        ).read_text(encoding="utf-8")
        examples = re.findall(r"```json\n(?P<plan>.*?)\n```", reference, re.DOTALL)
        self.assertEqual(len(examples), 3)
        with tempfile.TemporaryDirectory() as directory:
            amendment_path = Path(directory) / "amendment.json"
            amendment_path.write_text(examples[1], encoding="utf-8")
            reply_path = Path(directory) / "reply.json"
            reply_path.write_text(examples[2], encoding="utf-8")
            amendment = transaction.load_amendment(amendment_path)
            reply = transaction.load_reply(reply_path)
        self.assertIsInstance(amendment, transaction.AmendmentPlan)
        self.assertIsInstance(reply, transaction.ReplyPlan)
        self.assertEqual(amendment.finding_id, reply.finding_id)

    def test_documented_statuses_cover_all_success_results(self) -> None:
        reference = (
            Path(__file__).parent.parent / "references" / "github-publishing.md"
        ).read_text(encoding="utf-8")
        statuses = (
            "audit",
            "valid",
            "resume-ready",
            "noop-existing-snapshot",
            "published",
            "published-reconciled",
            "amended",
            "amended-reconciled",
            "replied",
            "replied-reconciled",
            "noop-existing-reply",
        )
        for status in statuses:
            with self.subTest(status=status):
                self.assertIn(f"- `{status}`:", reference)

    def test_zero_finding_summary_requires_three_evidence_entries(self) -> None:
        plan = make_plan(
            comments=False,
            summary=make_summary(
                evidence=(
                    transaction.ReviewEvidence(
                        "boundary-behavior", "Checked boundaries."
                    ),
                    transaction.ReviewEvidence(
                        "tests-validation", "Checked tests."
                    ),
                )
            ),
        )
        raw = plan_payload(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "thin-zero-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_plan_rejects_duplicate_evidence_areas(self) -> None:
        raw = plan_payload(make_plan())
        raw["summary"]["evidence"][1]["area"] = "boundary-behavior"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-evidence-area-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_plan_loader_rejects_a_repeated_thread_title(self) -> None:
        original = make_plan()
        title = original.comments[0].body.splitlines()[0].split(": ", 1)[1]
        plan = make_plan(
            summary=make_summary(
                notes=(transaction.ReviewNote("optional", title),)
            )
        )
        raw = plan_payload(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicated-summary-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_focused_profile_rejects_review_notes(self) -> None:
        plan = make_plan(
            profile="focused",
            summary=make_summary(
                notes=(transaction.ReviewNote("positive", "The rollback stays bounded."),)
            ),
        )
        raw = plan_payload(plan)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "focused-notes-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_plan_rejects_an_unknown_feedback_profile(self) -> None:
        raw = plan_payload(make_plan())
        raw["profile"] = "verbose"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unknown-profile-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_summary_fields_cannot_inject_markdown_structure(self) -> None:
        injected_values = (
            "### Replacement heading",
            "```text",
            "<details>",
            "---",
            "> Hidden receipt",
        )
        for injected in injected_values:
            with self.subTest(injected=injected):
                raw = plan_payload(make_plan())
                raw["summary"]["overview"] = injected
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "injected-summary-plan.json"
                    path.write_text(json.dumps(raw), encoding="utf-8")
                    with self.assertRaises(transaction.PlanError):
                        transaction.load_plan(path)

    def test_summary_accepts_one_trailing_validation_checkmark(self) -> None:
        raw = plan_payload(make_plan())
        raw["summary"]["evidence"][2]["detail"] += " ✅"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "validation-checkmark-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_plan(path)
        self.assertIn("✅", loaded.summary_body())

    def test_summary_rejects_misplaced_or_repeated_checkmarks(self) -> None:
        invalid_summaries = []

        misplaced = plan_payload(make_plan())
        misplaced["summary"]["overview"] += " ✅"
        invalid_summaries.append(misplaced)

        repeated = plan_payload(make_plan())
        repeated["summary"]["evidence"][2]["detail"] += " ✅ ✅"
        invalid_summaries.append(repeated)

        leading = plan_payload(make_plan())
        leading["summary"]["evidence"][2]["detail"] = "✅ Ran the focused tests."
        invalid_summaries.append(leading)

        for index, raw in enumerate(invalid_summaries):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "invalid-checkmark-plan.json"
                path.write_text(json.dumps(raw), encoding="utf-8")
                with self.assertRaises(transaction.PlanError):
                    transaction.load_plan(path)

    def test_assertive_profile_accepts_a_low_severity_suggestion(self) -> None:
        plan = make_plan(profile="assertive")
        raw = plan_payload(plan)
        raw["comments"][0].update(
            {
                "severity": "low",
                "disposition": "non-blocking",
                "category": "maintainability",
                "body": (
                    "suggestion (non-blocking, low, maintainability): Name the rollback phase\n\n"
                    "A named phase would make the recovery sequence easier to maintain."
                ),
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assertive-suggestion-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_plan(path)
        self.assertEqual(loaded.comments[0].severity, "low")
        self.assertIn(
            "| Findings | 0 blocking · 0 non-blocking · 0 questions · "
            "**1 suggestion** |",
            loaded.summary_body(),
        )

    def test_suggestion_only_review_still_requires_zero_finding_evidence(self) -> None:
        plan = make_plan(profile="assertive")
        raw = plan_payload(plan)
        raw["summary"]["evidence"] = raw["summary"]["evidence"][:2]
        raw["comments"][0].update(
            {
                "severity": "low",
                "disposition": "non-blocking",
                "category": "maintainability",
                "body": (
                    "suggestion (non-blocking, low, maintainability): Name the rollback phase\n\n"
                    "A named phase would make the recovery sequence easier to maintain."
                ),
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "thin-suggestion-only-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_balanced_profile_rejects_a_low_severity_suggestion(self) -> None:
        raw = plan_payload(make_plan())
        raw["comments"][0].update(
            {
                "severity": "low",
                "disposition": "non-blocking",
                "category": "maintainability",
                "body": (
                    "suggestion (non-blocking, low, maintainability): Name the rollback phase\n\n"
                    "A named phase would make the recovery sequence easier to maintain."
                ),
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "balanced-suggestion-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_low_severity_suggestion_cannot_block(self) -> None:
        raw = dict(make_plan().comments[0].__dict__)
        raw.update(
            {
                "severity": "low",
                "disposition": "blocking",
                "category": "maintainability",
                "body": (
                    "suggestion (blocking, low, maintainability): Name the rollback phase\n\n"
                    "A named phase would make the recovery sequence easier to maintain."
                ),
            }
        )
        with self.assertRaises(transaction.PlanError):
            transaction.parse_comment(raw, 0, "assertive")

    def test_same_snapshot_rerun_is_a_noop(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        review_id = client.add_review(plan)
        result = transaction.publish(client, self.ref, plan, "COMMENT")
        self.assertEqual(result["status"], "noop-existing-snapshot")
        self.assertEqual(result["review_id"], review_id)
        self.assertEqual(client.post_calls, [])

    def test_version_one_review_marker_still_blocks_same_snapshot_repost(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        review_id = client.add_review(plan)
        client.reviews[0]["body"] = client.reviews[0]["body"].replace(
            "gh-review-pr:review v=2", "gh-review-pr:review v=1"
        )

        result = transaction.publish(client, self.ref, plan, "COMMENT")

        self.assertEqual(result["status"], "noop-existing-snapshot")
        self.assertEqual(result["review_id"], review_id)
        self.assertEqual(client.post_calls, [])

    def test_owned_finding_body_can_be_amended_without_changing_marker(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        review_id = client.add_review(plan)
        original_marker = transaction.finding_marker_data(client.comments[0]["body"])

        result = transaction.amend_comment(
            client, self.ref, make_amendment(review_id)
        )

        self.assertEqual(result["status"], "amended")
        self.assertEqual(len(client.patch_calls), 1)
        self.assertEqual(
            transaction.finding_marker_data(client.comments[0]["body"]),
            original_marker,
        )
        self.assertEqual(
            transaction.without_marker(
                client.comments[0]["body"], transaction.FINDING_MARKER_RE
            ),
            make_amendment(review_id).body,
        )

    def test_version_one_markers_remain_maintainable(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.reviews[0]["body"] = client.reviews[0]["body"].replace(
            "gh-review-pr:review v=2", "gh-review-pr:review v=1"
        )
        client.comments[0]["body"] = client.comments[0]["body"].replace(
            "gh-review-pr:finding v=2", "gh-review-pr:finding v=1"
        )

        result = transaction.amend_comment(
            client, self.ref, make_amendment(review_id)
        )

        self.assertEqual(result["status"], "amended")
        marker = transaction.finding_marker_data(client.comments[0]["body"])
        self.assertEqual(marker["version"], "1")

    def test_ambiguous_amendment_reconciles_without_retry(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.patch_failure_after_apply = True

        result = transaction.amend_comment(
            client, self.ref, make_amendment(review_id)
        )

        self.assertEqual(result["status"], "amended-reconciled")
        self.assertEqual(len(client.patch_calls), 1)

    def test_human_comment_cannot_be_amended(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.comments[0]["body"] = "Human-authored note"

        with self.assertRaises(transaction.SafetyError):
            transaction.amend_comment(
                client, self.ref, make_amendment(review_id)
            )

        self.assertEqual(client.patch_calls, [])

    def test_amendment_cannot_change_finding_classification(self) -> None:
        replacements = (
            (
                "disposition",
                "issue (non-blocking, high, data-integrity): "
                "Clarify the failure path\n\n"
                "The changed exception propagation makes the failure reachable.",
            ),
            (
                "severity",
                "issue (blocking, medium, data-integrity): Clarify the failure path\n\n"
                "The changed exception propagation makes the failure reachable.",
            ),
            (
                "category",
                "issue (blocking, high, reliability): Clarify the failure path\n\n"
                "The changed exception propagation makes the failure reachable.",
            ),
        )
        for label, body in replacements:
            with self.subTest(label=label):
                client = FakeGitHubClient()
                review_id = client.add_review(make_plan())

                with self.assertRaises(transaction.SafetyError):
                    transaction.amend_comment(
                        client, self.ref, make_amendment(review_id, body=body)
                    )

                self.assertEqual(client.patch_calls, [])

    def test_amendment_stops_when_current_head_changes_before_write(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.head_after_comment_list = NEW_HEAD_SHA

        with self.assertRaises(transaction.SafetyError):
            transaction.amend_comment(
                client, self.ref, make_amendment(review_id)
            )

        self.assertEqual(client.patch_calls, [])

    def test_owned_finding_can_receive_one_verified_reply(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        reply = make_reply(review_id)

        result = transaction.reply_to_owned_finding(client, self.ref, reply)
        second = transaction.reply_to_owned_finding(client, self.ref, reply)

        self.assertEqual(result["status"], "replied")
        self.assertEqual(second["status"], "noop-existing-reply")
        self.assertEqual(result["review_head_sha"], HEAD_SHA)
        self.assertEqual(result["current_head_sha"], HEAD_SHA)
        reply_calls = [
            value for value in client.post_calls if value.endswith("/replies")
        ]
        self.assertEqual(len(reply_calls), 1)

    def test_ambiguous_owned_reply_reconciles_without_retry(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.reply_failure_after_apply = True
        reply = make_reply(review_id)

        result = transaction.reply_to_owned_finding(client, self.ref, reply)

        self.assertEqual(result["status"], "replied-reconciled")
        reply_calls = [
            value for value in client.post_calls if value.endswith("/replies")
        ]
        self.assertEqual(len(reply_calls), 1)

    def test_owned_finding_reply_allows_a_newer_pr_head(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.head_sha = NEW_HEAD_SHA

        result = transaction.reply_to_owned_finding(
            client, self.ref, make_reply(review_id)
        )

        self.assertEqual(result["status"], "replied")
        self.assertEqual(result["review_head_sha"], HEAD_SHA)
        self.assertEqual(result["current_head_sha"], NEW_HEAD_SHA)

    def test_reply_stops_when_current_head_changes_before_write(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.head_after_comment_list = NEW_HEAD_SHA

        with self.assertRaises(transaction.SafetyError):
            transaction.reply_to_owned_finding(
                client, self.ref, make_reply(review_id)
            )

        reply_calls = [
            value for value in client.post_calls if value.endswith("/replies")
        ]
        self.assertEqual(reply_calls, [])

    def test_human_comment_cannot_receive_an_owned_finding_reply(self) -> None:
        client = FakeGitHubClient()
        review_id = client.add_review(make_plan())
        client.comments[0]["body"] = "Human-authored note"

        with self.assertRaises(transaction.SafetyError):
            transaction.reply_to_owned_finding(
                client, self.ref, make_reply(review_id)
            )

        reply_calls = [
            value for value in client.post_calls if value.endswith("/replies")
        ]
        self.assertEqual(reply_calls, [])

    def test_multiple_same_snapshot_reviews_stop_without_another_write(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        client.add_review(plan)
        client.add_review(plan)
        with self.assertRaises(transaction.SafetyError):
            transaction.publish(client, self.ref, plan, "COMMENT")
        self.assertEqual(client.post_calls, [])

    def test_dismissed_same_snapshot_review_still_blocks_reposting(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        review_id = client.add_review(plan, state="DISMISSED")
        result = transaction.publish(client, self.ref, plan, "COMMENT")
        self.assertEqual(result["status"], "noop-existing-snapshot")
        self.assertEqual(result["review_id"], review_id)
        self.assertEqual(client.post_calls, [])

    def test_same_head_with_a_different_base_is_a_new_snapshot(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan(comments=False)
        prior_plan = transaction.ReviewPlan(
            "d" * 40, plan.head_sha, plan.profile, plan.summary, ()
        )
        client.add_review(prior_plan)

        result = transaction.publish(client, self.ref, plan, "COMMENT")

        self.assertEqual(result["status"], "published")
        self.assertEqual(len(client.reviews), 2)

    def test_invalid_anchor_submits_nothing(self) -> None:
        client = FakeGitHubClient()
        with self.assertRaises(transaction.SafetyError):
            transaction.publish(client, self.ref, make_plan(line=99), "COMMENT")
        self.assertEqual(client.post_calls, [])
        self.assertEqual(client.reviews, [])

    def test_null_line_is_rejected_before_any_remote_call(self) -> None:
        raw = dict(make_plan().comments[0].__dict__)
        raw["line"] = None
        with self.assertRaises(transaction.PlanError):
            transaction.parse_comment(raw, 0)

    def test_head_change_deletes_owned_pending_and_stops(self) -> None:
        client = FakeGitHubClient()
        client.head_after_create = NEW_HEAD_SHA
        with self.assertRaises(transaction.VerificationError):
            transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(len(client.delete_calls), 1)
        self.assertEqual(client.reviews, [])
        self.assertEqual(client.comments, [])

    def test_legacy_position_is_verified_when_line_and_side_are_null(self) -> None:
        client = FakeGitHubClient()
        client.created_comment_overrides = {
            "line": None,
            "original_line": 2,
            "side": None,
            "position": 2,
            "original_position": 2,
            "commit_id": HEAD_SHA,
            "original_commit_id": HEAD_SHA,
        }

        result = transaction.publish(client, self.ref, make_plan(), "COMMENT")

        self.assertEqual(result["status"], "published")
        self.assertEqual(result["inline_count"], 1)
        self.assertEqual(client.delete_calls, [])

    def test_wrong_legacy_position_reports_locators_and_deletes_pending(self) -> None:
        client = FakeGitHubClient()
        client.created_comment_overrides = {
            "line": None,
            "original_line": None,
            "side": None,
            "position": 4,
            "original_position": 4,
            "commit_id": HEAD_SHA,
            "original_commit_id": HEAD_SHA,
        }

        with self.assertRaises(transaction.VerificationError) as raised:
            transaction.publish(client, self.ref, make_plan(), "COMMENT")

        message = str(raised.exception)
        self.assertIn('"line":null', message)
        self.assertIn('"original_position":4', message)
        self.assertNotIn("Preserve existing state", message)
        self.assertEqual(len(client.delete_calls), 1)
        self.assertEqual(client.reviews, [])
        self.assertEqual(client.comments, [])

    def test_legacy_position_from_another_commit_is_rejected(self) -> None:
        client = FakeGitHubClient()
        client.created_comment_overrides = {
            "line": None,
            "side": None,
            "position": 2,
            "original_position": 2,
            "commit_id": NEW_HEAD_SHA,
            "original_commit_id": NEW_HEAD_SHA,
        }

        with self.assertRaises(transaction.VerificationError):
            transaction.publish(client, self.ref, make_plan(), "COMMENT")

        self.assertEqual(len(client.delete_calls), 1)
        self.assertEqual(client.reviews, [])

    def test_permission_failure_has_no_fallback_write(self) -> None:
        client = FakeGitHubClient()
        client.create_failure = "before"
        with self.assertRaises(transaction.GitHubError):
            transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(client.post_calls, [f"{client.pull_endpoint()}/reviews"])
        self.assertEqual(client.reviews, [])
        self.assertEqual(client.comments, [])

    def test_ambiguous_create_reconciles_existing_pending(self) -> None:
        client = FakeGitHubClient()
        client.create_failure = "after"
        result = transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(result["status"], "published")
        self.assertEqual(client.reviews[0]["state"], "COMMENTED")
        self.assertEqual(len(client.reviews), 1)

    def test_ambiguous_submit_reconciles_final_state_without_retry(self) -> None:
        client = FakeGitHubClient()
        client.submit_failure_after_apply = True
        result = transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(result["status"], "published-reconciled")
        event_calls = [
            value for value in client.post_calls if value.endswith("/events")
        ]
        self.assertEqual(len(event_calls), 1)

    def test_human_pending_review_is_untouched(self) -> None:
        client = FakeGitHubClient()
        client.reviews.append(
            {
                "id": 73,
                "state": "PENDING",
                "commit_id": HEAD_SHA,
                "body": "My draft notes",
                "user": {"login": client.login},
            }
        )
        with self.assertRaises(transaction.SafetyError):
            transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(client.post_calls, [])
        self.assertEqual(client.delete_calls, [])
        self.assertEqual(client.reviews[0]["body"], "My draft notes")

    def test_prior_finding_id_blocks_repost_on_new_head(self) -> None:
        client = FakeGitHubClient()
        old_plan = transaction.ReviewPlan(
            BASE_SHA,
            NEW_HEAD_SHA,
            make_plan().profile,
            make_plan().summary,
            make_plan().comments,
        )
        client.add_review(old_plan)
        with self.assertRaises(transaction.SafetyError):
            transaction.publish(client, self.ref, make_plan(), "COMMENT")
        self.assertEqual(client.post_calls, [])

    def test_zero_finding_review_is_valid(self) -> None:
        client = FakeGitHubClient()
        result = transaction.publish(
            client, self.ref, make_plan(comments=False), "COMMENT"
        )
        self.assertEqual(result["status"], "published")
        self.assertEqual(result["profile"], "balanced")
        self.assertEqual(result["inline_count"], 0)
        self.assertEqual(client.comments, [])

    def test_request_changes_requires_a_blocking_finding(self) -> None:
        client = FakeGitHubClient()
        with self.assertRaises(transaction.PlanError):
            transaction.publish(
                client, self.ref, make_plan(comments=False), "REQUEST_CHANGES"
            )
        self.assertEqual(client.post_calls, [])

    def test_approve_rejects_a_blocking_finding(self) -> None:
        client = FakeGitHubClient()
        with self.assertRaises(transaction.PlanError):
            transaction.publish(client, self.ref, make_plan(), "APPROVE")
        self.assertEqual(client.post_calls, [])

    def test_probable_secret_literal_is_rejected(self) -> None:
        raw = {
            "finding_id": "redact-live-secret",
            "path": "src/config.py",
            "line": 2,
            "side": "RIGHT",
            "severity": "critical",
            "confidence": "high",
            "disposition": "blocking",
            "category": "security",
            "body": (
                "issue (blocking, critical, security): Remove the embedded credential\n\n"
                "The new value sets password = 'super-secret-value-12345'. Redact and rotate it."
            ),
        }
        with self.assertRaises(transaction.PlanError):
            transaction.parse_comment(raw, 0)


if __name__ == "__main__":
    unittest.main()
