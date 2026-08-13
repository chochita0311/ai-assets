#!/usr/bin/env python3
"""Publish one PR description with authorization and concurrency safeguards."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


_PR_URL_RE = re.compile(
    r"https://(?P<host>[A-Za-z0-9.-]+)/"
    r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)/pull/"
    r"(?P<number>[1-9][0-9]*)"
)
_HOST_LABEL_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?")


class PublicationError(RuntimeError):
    """Base class for safe publication stops."""

    exit_code = 2


class AuthorizationError(PublicationError):
    """Publication was not explicitly authorized in the current turn."""


class TargetError(PublicationError):
    """The PR target is not an exact full URL."""


class CandidateError(PublicationError):
    """The candidate or backup file is unsafe."""


class ConcurrentUpdateError(PublicationError):
    """The remote PR changed after the initial capture."""

    exit_code = 3


class RemoteError(PublicationError):
    """A read or write through gh failed."""

    exit_code = 4


class VerificationError(PublicationError):
    """The observed body does not match the published candidate."""

    exit_code = 5


@dataclass(frozen=True)
class PullRequestTarget:
    url: str
    host: str

    @classmethod
    def parse(cls, value: str) -> "PullRequestTarget":
        match = _PR_URL_RE.fullmatch(value) if isinstance(value, str) else None
        if match is None:
            raise TargetError(
                "PR target must exactly match "
                "https://<host>/<owner>/<repo>/pull/<positive-number>"
            )
        host = match.group("host")
        labels = host.split(".")
        if (
            len(host) > 253
            or any(len(label) > 63 for label in labels)
            or any(_HOST_LABEL_RE.fullmatch(label) is None for label in labels)
        ):
            raise TargetError("PR target contains an invalid hostname")
        return cls(url=value, host=host.lower())


@dataclass(frozen=True)
class PullRequestSnapshot:
    body: str
    updated_at: str


class PullRequestRemote(Protocol):
    def fetch(self, target: PullRequestTarget) -> PullRequestSnapshot: ...

    def publish(self, target: PullRequestTarget, candidate_file: Path) -> None: ...


Runner = Callable[..., subprocess.CompletedProcess[str]]


class GhRemote:
    """Minimal file-only gh adapter used by the real CLI."""

    def __init__(self, runner: Runner = subprocess.run) -> None:
        self._runner = runner

    def _run(
        self, target: PullRequestTarget, arguments: Sequence[str]
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["GH_HOST"] = target.host
        command = ["gh", *arguments]
        try:
            completed = self._runner(
                command,
                capture_output=True,
                check=False,
                env=environment,
                shell=False,
                text=True,
            )
        except OSError as error:
            raise RemoteError(f"could not run gh: {error}") from error
        if completed.returncode != 0:
            detail = completed.stderr.strip() or "no error detail"
            raise RemoteError(f"gh command failed: {detail}")
        return completed

    def fetch(self, target: PullRequestTarget) -> PullRequestSnapshot:
        completed = self._run(
            target,
            ["pr", "view", target.url, "--json", "body,updatedAt"],
        )
        try:
            value = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise RemoteError("gh returned invalid JSON") from error
        if not isinstance(value, Mapping):
            raise RemoteError("gh returned a non-object PR snapshot")
        body = value.get("body")
        updated_at = value.get("updatedAt")
        if not isinstance(body, str) or not isinstance(updated_at, str) or not updated_at:
            raise RemoteError("gh PR snapshot is missing body or updatedAt")
        return PullRequestSnapshot(body=body, updated_at=updated_at)

    def publish(self, target: PullRequestTarget, candidate_file: Path) -> None:
        self._run(
            target,
            ["pr", "edit", target.url, "--body-file", str(candidate_file)],
        )


def _read_candidate(path: Path) -> str:
    if not path.is_file():
        raise CandidateError(f"candidate file does not exist: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise CandidateError(f"could not read candidate file: {path}") from error


def _write_backup(path: Path, body: str) -> None:
    try:
        with path.open("x", encoding="utf-8", newline="") as stream:
            stream.write(body)
    except OSError as error:
        raise CandidateError(f"could not create exclusive backup file: {path}") from error


def _checked_snapshot(
    remote: PullRequestRemote, target: PullRequestTarget
) -> PullRequestSnapshot:
    snapshot = remote.fetch(target)
    if (
        not isinstance(snapshot, PullRequestSnapshot)
        or not isinstance(snapshot.body, str)
        or not isinstance(snapshot.updated_at, str)
        or not snapshot.updated_at
    ):
        raise RemoteError("remote returned an invalid PR snapshot")
    return snapshot


def publish_pr_description_transaction(
    *,
    pr_url: str,
    candidate_file: str | Path,
    backup_file: str | Path,
    publish_current_turn: bool,
    allow_clear_current_turn: bool = False,
    remote: PullRequestRemote,
) -> PullRequestSnapshot:
    """Run one authorized, single-write PR-description transaction."""

    if not publish_current_turn:
        raise AuthorizationError(
            "publication requires explicit authorization from the current turn"
        )
    target = PullRequestTarget.parse(pr_url)
    candidate_path = Path(candidate_file).resolve()
    backup_path = Path(backup_file).resolve()
    if candidate_path == backup_path:
        raise CandidateError("candidate and backup files must be separate")

    candidate_body = _read_candidate(candidate_path)
    if candidate_body == "" and not allow_clear_current_turn:
        raise CandidateError(
            "empty candidate requires an explicit current-turn clear request"
        )

    initial = _checked_snapshot(remote, target)
    _write_backup(backup_path, initial.body)

    if _read_candidate(candidate_path) != candidate_body:
        raise CandidateError("candidate file changed after validation")
    current = _checked_snapshot(remote, target)
    if current.updated_at != initial.updated_at:
        raise ConcurrentUpdateError(
            "PR updatedAt changed after capture; no description write was attempted"
        )

    remote.publish(target, candidate_path)
    observed = _checked_snapshot(remote, target)
    if observed.body != candidate_body:
        raise VerificationError(
            "published PR body does not exactly match the candidate; "
            "no retry or restore was attempted"
        )
    return observed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr_url", help="Exact full PR URL")
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--backup-file", required=True, type=Path)
    parser.add_argument(
        "--publish-current-turn",
        action="store_true",
        help="Confirm explicit publication authorization in the current turn",
    )
    parser.add_argument(
        "--allow-clear-current-turn",
        action="store_true",
        help="Confirm that the current turn explicitly requested an empty body",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        observed = publish_pr_description_transaction(
            pr_url=arguments.pr_url,
            candidate_file=arguments.candidate_file,
            backup_file=arguments.backup_file,
            publish_current_turn=arguments.publish_current_turn,
            allow_clear_current_turn=arguments.allow_clear_current_turn,
            remote=GhRemote(),
        )
    except PublicationError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code
    print(
        json.dumps(
            {
                "status": "verified",
                "pr_url": arguments.pr_url,
                "updatedAt": observed.updated_at,
                "backup_file": str(arguments.backup_file.resolve()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
