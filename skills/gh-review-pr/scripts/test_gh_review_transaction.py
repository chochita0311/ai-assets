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


def make_plan(*, line: int = 2, comments: bool = True) -> transaction.ReviewPlan:
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
        summary=(
            "## Review summary\n\nReviewed one changed file at `bbbbbbb`; "
            f"the review found {1 if comments else 0} blocking, 0 non-blocking, "
            "and 0 question findings."
        ),
        comments=findings,
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
        self.delete_calls: list[str] = []
        self.create_failure: str | None = None
        self.submit_failure_after_apply = False
        self.head_after_create: str | None = None

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
            return [dict(value) for value in self.comments]
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
                    **comment_payload,
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
        raise AssertionError(f"unexpected POST endpoint: {endpoint}")

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

    def test_plan_loader_accepts_the_documented_schema(self) -> None:
        plan = make_plan()
        raw = {
            "schema_version": transaction.SCHEMA_VERSION,
            "base_sha": plan.base_sha,
            "head_sha": plan.head_sha,
            "summary": plan.summary,
            "comments": [comment.__dict__ for comment in plan.comments],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            loaded = transaction.load_plan(path)
        self.assertEqual(loaded, plan)

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

    def test_plan_loader_rejects_incorrect_summary_counts(self) -> None:
        plan = make_plan()
        raw = {
            "schema_version": transaction.SCHEMA_VERSION,
            "base_sha": plan.base_sha,
            "head_sha": plan.head_sha,
            "summary": plan.summary.replace("1 blocking", "0 blocking"),
            "comments": [comment.__dict__ for comment in plan.comments],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-count-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_plan_loader_rejects_a_repeated_thread_title(self) -> None:
        plan = make_plan()
        title = plan.comments[0].body.splitlines()[0].split(": ", 1)[1]
        raw = {
            "schema_version": transaction.SCHEMA_VERSION,
            "base_sha": plan.base_sha,
            "head_sha": plan.head_sha,
            "summary": plan.summary[:-1] + f"; {title}.",
            "comments": [comment.__dict__ for comment in plan.comments],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicated-summary-plan.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(transaction.PlanError):
                transaction.load_plan(path)

    def test_same_snapshot_rerun_is_a_noop(self) -> None:
        client = FakeGitHubClient()
        plan = make_plan()
        review_id = client.add_review(plan)
        result = transaction.publish(client, self.ref, plan, "COMMENT")
        self.assertEqual(result["status"], "noop-existing-snapshot")
        self.assertEqual(result["review_id"], review_id)
        self.assertEqual(client.post_calls, [])

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
        prior_plan = transaction.ReviewPlan("d" * 40, plan.head_sha, plan.summary, ())
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
