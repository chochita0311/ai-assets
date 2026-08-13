#!/usr/bin/env python3
"""Offline tests for the PR-description publication transaction."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import pr_description_transaction as transaction


PR_URL = "https://github.example.com/octo/widgets/pull/17"


class FakeRemote:
    def __init__(
        self,
        *,
        recheck_updated_at: str | None = None,
        post_write_body: str | None = None,
    ) -> None:
        self.body = "original body"
        self.updated_at = "2026-08-13T00:00:00Z"
        self.recheck_updated_at = recheck_updated_at
        self.post_write_body = post_write_body
        self.fetch_count = 0
        self.writes: list[str] = []

    def fetch(
        self, target: transaction.PullRequestTarget
    ) -> transaction.PullRequestSnapshot:
        self.fetch_count += 1
        marker = self.updated_at
        if self.fetch_count == 2 and self.recheck_updated_at is not None:
            marker = self.recheck_updated_at
        return transaction.PullRequestSnapshot(body=self.body, updated_at=marker)

    def publish(
        self, target: transaction.PullRequestTarget, candidate_file: Path
    ) -> None:
        candidate = candidate_file.read_text(encoding="utf-8")
        self.writes.append(candidate)
        self.body = candidate if self.post_write_body is None else self.post_write_body
        self.updated_at = "2026-08-13T00:00:01Z"


class FakeRunner:
    def __init__(self, candidate_body: str) -> None:
        self.candidate_body = candidate_body
        self.calls: list[tuple[list[str], dict[str, object]]] = []
        self.view_count = 0

    def __call__(self, command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.calls.append((command, kwargs))
        if command[1:3] == ["pr", "view"]:
            self.view_count += 1
            body = self.candidate_body if self.view_count == 3 else "original body"
            marker = "after" if self.view_count == 3 else "before"
            stdout = json.dumps({"body": body, "updatedAt": marker})
        elif command[1:3] == ["pr", "edit"]:
            stdout = ""
        else:
            raise AssertionError(f"unexpected command: {command}")
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")


class PublicationTransactionTests(unittest.TestCase):
    def _paths(self, directory: str, body: str) -> tuple[Path, Path]:
        candidate = Path(directory, "candidate.md")
        candidate.write_text(body, encoding="utf-8")
        return candidate, Path(directory, "backup.md")

    def test_empty_candidate_is_rejected_before_writes_unless_clear_is_allowed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "")
            rejected_remote = FakeRemote()
            with self.assertRaises(transaction.CandidateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    publish_current_turn=True,
                    remote=rejected_remote,
                )
            self.assertEqual(rejected_remote.fetch_count, 0)
            self.assertEqual(rejected_remote.writes, [])
            self.assertFalse(backup.exists())

            allowed_remote = FakeRemote()
            observed = transaction.publish_pr_description_transaction(
                pr_url=PR_URL,
                candidate_file=candidate,
                backup_file=backup,
                publish_current_turn=True,
                allow_clear_current_turn=True,
                remote=allowed_remote,
            )
            self.assertEqual(allowed_remote.writes, [""])
            self.assertEqual(observed.body, "")
            self.assertEqual(backup.read_text(encoding="utf-8"), "original body")

    def test_changed_concurrency_marker_stops_with_zero_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote(recheck_updated_at="changed")
            with self.assertRaises(transaction.ConcurrentUpdateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 2)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), "original body")

    def test_post_write_mismatch_fails_after_exactly_one_write_without_recovery(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote(post_write_body="unexpected body")
            with self.assertRaises(transaction.VerificationError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 3)
            self.assertEqual(remote.writes, ["candidate body"])
            self.assertEqual(remote.body, "unexpected body")
            self.assertEqual(backup.read_text(encoding="utf-8"), "original body")

    def test_authorization_and_exact_full_url_fail_before_remote_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote()
            with self.assertRaises(transaction.AuthorizationError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    publish_current_turn=False,
                    remote=remote,
                )
            with self.assertRaises(transaction.TargetError):
                transaction.publish_pr_description_transaction(
                    pr_url="octo/widgets#17",
                    candidate_file=candidate,
                    backup_file=backup,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 0)
            self.assertEqual(remote.writes, [])

    def test_ghes_adapter_uses_full_url_file_only_edit_and_gh_host(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            runner = FakeRunner("candidate body")
            transaction.publish_pr_description_transaction(
                pr_url=PR_URL,
                candidate_file=candidate,
                backup_file=backup,
                publish_current_turn=True,
                remote=transaction.GhRemote(runner),
            )

            edit_commands = [
                command
                for command, _ in runner.calls
                if command[1:3] == ["pr", "edit"]
            ]
            self.assertEqual(
                edit_commands,
                [
                    [
                        "gh",
                        "pr",
                        "edit",
                        PR_URL,
                        "--body-file",
                        str(candidate.resolve()),
                    ]
                ],
            )
            for command, kwargs in runner.calls:
                self.assertIs(kwargs["shell"], False)
                environment = kwargs["env"]
                self.assertIsInstance(environment, dict)
                self.assertEqual(environment["GH_HOST"], "github.example.com")
                self.assertNotIn("--body", command)
                self.assertNotIn("-", command)


if __name__ == "__main__":
    unittest.main()
