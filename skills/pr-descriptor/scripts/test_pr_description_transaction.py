#!/usr/bin/env python3
"""Offline tests for the PR-description publication transaction."""

from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from collections.abc import Callable
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import pr_description_transaction as transaction


PR_URL = "https://github.example.com/octo/widgets/pull/17"
ORIGINAL_BODY = "original body"
CAPTURED_UPDATED_AT = "2026-08-13T00:00:00Z"


class FakeRemote:
    def __init__(
        self,
        *,
        body: str = ORIGINAL_BODY,
        updated_at: str = CAPTURED_UPDATED_AT,
        recheck_updated_at: str | None = None,
        recheck_body: str | None = None,
        post_write_body: str | None = None,
        on_first_fetch: Callable[[], None] | None = None,
    ) -> None:
        self.body = body
        self.updated_at = updated_at
        self.recheck_updated_at = recheck_updated_at
        self.recheck_body = recheck_body
        self.post_write_body = post_write_body
        self.on_first_fetch = on_first_fetch
        self.fetch_count = 0
        self.writes: list[str] = []

    def fetch(
        self, target: transaction.PullRequestTarget
    ) -> transaction.PullRequestSnapshot:
        self.fetch_count += 1
        if self.fetch_count == 1 and self.on_first_fetch is not None:
            self.on_first_fetch()
        body = self.body
        marker = self.updated_at
        if self.fetch_count == 2:
            if self.recheck_updated_at is not None:
                marker = self.recheck_updated_at
            if self.recheck_body is not None:
                body = self.recheck_body
        return transaction.PullRequestSnapshot(body=body, updated_at=marker)

    def publish(
        self, target: transaction.PullRequestTarget, candidate_file: Path
    ) -> None:
        with candidate_file.open(encoding="utf-8", newline="") as stream:
            candidate = stream.read()
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
            body = self.candidate_body if self.view_count == 3 else ORIGINAL_BODY
            marker = "after" if self.view_count == 3 else "before"
            stdout = json.dumps({"body": body, "updatedAt": marker})
        elif command[1:3] == ["pr", "edit"]:
            stdout = ""
        else:
            raise AssertionError(f"unexpected command: {command}")
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")


class PublicationTransactionTests(unittest.TestCase):
    def _paths(
        self, directory: str, body: str, backup_body: str = ORIGINAL_BODY
    ) -> tuple[Path, Path]:
        backup = Path(directory, "backup.md")
        backup.write_text(backup_body, encoding="utf-8", newline="")
        candidate = Path(directory, "candidate.md")
        candidate.write_text(body, encoding="utf-8", newline="")
        return candidate, backup

    def test_matching_capture_publishes_and_preserves_exact_backup(self) -> None:
        for original_body in ("original\r\nbody\r\n", ""):
            with self.subTest(original_body=original_body):
                with tempfile.TemporaryDirectory() as directory:
                    candidate_body = "candidate\r\nbody\r\n"
                    candidate, backup = self._paths(
                        directory, candidate_body, original_body
                    )
                    backup_bytes = backup.read_bytes()
                    remote = FakeRemote(body=original_body)
                    observed = transaction.publish_pr_description_transaction(
                        pr_url=PR_URL,
                        candidate_file=candidate,
                        backup_file=backup,
                        expected_updated_at=CAPTURED_UPDATED_AT,
                        publish_current_turn=True,
                        remote=remote,
                    )
                    self.assertEqual(remote.fetch_count, 3)
                    self.assertEqual(remote.writes, [candidate_body])
                    self.assertEqual(observed.body, candidate_body)
                    self.assertEqual(backup.read_bytes(), backup_bytes)

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
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=rejected_remote,
                )
            self.assertEqual(rejected_remote.fetch_count, 0)
            self.assertEqual(rejected_remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

            allowed_remote = FakeRemote()
            observed = transaction.publish_pr_description_transaction(
                pr_url=PR_URL,
                candidate_file=candidate,
                backup_file=backup,
                expected_updated_at=CAPTURED_UPDATED_AT,
                publish_current_turn=True,
                allow_clear_current_turn=True,
                remote=allowed_remote,
            )
            self.assertEqual(allowed_remote.writes, [""])
            self.assertEqual(observed.body, "")
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_update_during_drafting_stops_on_first_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate from original body")
            remote = FakeRemote(body="another actor's edit", updated_at="changed")
            with self.assertRaises(transaction.ConcurrentUpdateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 1)
            self.assertEqual(remote.writes, [])
            self.assertEqual(remote.body, "another actor's edit")
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_wrong_marker_or_backup_stops_on_first_fetch(self) -> None:
        for marker, body in (
            ("wrong marker", ORIGINAL_BODY),
            (CAPTURED_UPDATED_AT, "wrong backup body"),
        ):
            with self.subTest(marker=marker, body=body):
                with tempfile.TemporaryDirectory() as directory:
                    candidate, backup = self._paths(directory, "candidate body", body)
                    remote = FakeRemote()
                    with self.assertRaises(transaction.ConcurrentUpdateError):
                        transaction.publish_pr_description_transaction(
                            pr_url=PR_URL,
                            candidate_file=candidate,
                            backup_file=backup,
                            expected_updated_at=marker,
                            publish_current_turn=True,
                            remote=remote,
                        )
                    self.assertEqual(remote.fetch_count, 1)
                    self.assertEqual(remote.writes, [])
                    self.assertEqual(backup.read_text(encoding="utf-8"), body)

    def test_changed_concurrency_marker_stops_with_zero_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote(recheck_updated_at="changed")
            with self.assertRaises(transaction.ConcurrentUpdateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 2)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_changed_body_with_same_marker_stops_at_recheck(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote(recheck_body="changed without a new marker")
            with self.assertRaises(transaction.ConcurrentUpdateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 2)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_missing_or_nonfile_backup_stops_without_creating_it(self) -> None:
        for backup_is_directory in (False, True):
            with self.subTest(backup_is_directory=backup_is_directory):
                with tempfile.TemporaryDirectory() as directory:
                    candidate, backup = self._paths(directory, "candidate body")
                    backup.unlink()
                    if backup_is_directory:
                        backup.mkdir()
                    remote = FakeRemote()
                    with self.assertRaises(transaction.CandidateError):
                        transaction.publish_pr_description_transaction(
                            pr_url=PR_URL,
                            candidate_file=candidate,
                            backup_file=backup,
                            expected_updated_at=CAPTURED_UPDATED_AT,
                            publish_current_turn=True,
                            remote=remote,
                        )
                    self.assertEqual(remote.fetch_count, 0)
                    self.assertEqual(remote.writes, [])
                    self.assertEqual(backup.exists(), backup_is_directory)

    def test_missing_or_empty_marker_fails_before_remote_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote()
            arguments = {
                "pr_url": PR_URL,
                "candidate_file": candidate,
                "backup_file": backup,
                "publish_current_turn": True,
                "remote": remote,
            }
            with self.assertRaises(TypeError):
                transaction.publish_pr_description_transaction(**arguments)
            for marker in ("", " \t", None):
                with self.subTest(marker=marker):
                    with self.assertRaises(transaction.CandidateError):
                        transaction.publish_pr_description_transaction(
                            **arguments, expected_updated_at=marker
                        )
            self.assertEqual(remote.fetch_count, 0)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_cli_requires_the_captured_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            arguments = [
                PR_URL,
                "--candidate-file",
                str(candidate),
                "--backup-file",
                str(backup),
                "--publish-current-turn",
            ]
            remote = FakeRemote()
            with patch.object(transaction, "GhRemote", return_value=remote):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as missing:
                        transaction.main(arguments)
                    self.assertEqual(missing.exception.code, 2)
                    self.assertEqual(
                        transaction.main(arguments + ["--expected-updated-at", ""]),
                        2,
                    )
            self.assertEqual(remote.fetch_count, 0)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_missing_candidate_or_shared_backup_path_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            candidate.unlink()
            remote = FakeRemote()
            for candidate_path in (candidate, backup):
                with self.subTest(candidate_path=candidate_path):
                    with self.assertRaises(transaction.CandidateError):
                        transaction.publish_pr_description_transaction(
                            pr_url=PR_URL,
                            candidate_file=candidate_path,
                            backup_file=backup,
                            expected_updated_at=CAPTURED_UPDATED_AT,
                            publish_current_turn=True,
                            remote=remote,
                        )
            self.assertEqual(remote.fetch_count, 0)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_candidate_changed_after_validation_stops_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")

            def change_candidate() -> None:
                candidate.write_text("changed candidate", encoding="utf-8")

            remote = FakeRemote(on_first_fetch=change_candidate)
            with self.assertRaises(transaction.CandidateError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 1)
            self.assertEqual(remote.writes, [])
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

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
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=True,
                    remote=remote,
                )
            self.assertEqual(remote.fetch_count, 3)
            self.assertEqual(remote.writes, ["candidate body"])
            self.assertEqual(remote.body, "unexpected body")
            self.assertEqual(backup.read_text(encoding="utf-8"), ORIGINAL_BODY)

    def test_authorization_and_exact_full_url_fail_before_remote_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate, backup = self._paths(directory, "candidate body")
            remote = FakeRemote()
            with self.assertRaises(transaction.AuthorizationError):
                transaction.publish_pr_description_transaction(
                    pr_url=PR_URL,
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
                    publish_current_turn=False,
                    remote=remote,
                )
            with self.assertRaises(transaction.TargetError):
                transaction.publish_pr_description_transaction(
                    pr_url="octo/widgets#17",
                    candidate_file=candidate,
                    backup_file=backup,
                    expected_updated_at=CAPTURED_UPDATED_AT,
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
                expected_updated_at="before",
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
