#!/usr/bin/env python3
"""Regression tests for validate_skill_packages.py."""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import validate_skill_packages as validator


class SkillPackageValidatorTests(unittest.TestCase):
    def make_package(
        self,
        skills_root: Path,
        directory_name: str,
        *,
        declared_name: str | None = None,
        body: str = "",
    ) -> Path:
        package = skills_root / directory_name
        package.mkdir(parents=True)
        name = declared_name or directory_name
        (package / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test package.\n---\n\n# Test\n\n{body}\n",
            encoding="utf-8",
        )
        return package

    def test_current_repository_packages_pass(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        report = validator.validate_packages(repository_root / "skills")
        self.assertEqual(report.findings, [])
        self.assertGreater(report.package_count, 0)

    def test_package_name_must_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root, "alpha-skill", declared_name="different-skill"
            )

            report = validator.validate_packages(skills_root)

        self.assertFalse(report.ok)
        self.assertIn("package-name", {finding.code for finding in report.findings})

    def test_self_reference_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root, "alpha-skill", body="Use $alpha-skill for this task."
            )

            report = validator.validate_packages(skills_root)

        self.assertTrue(report.ok)
        self.assertEqual(report.self_reference_count, 1)

    def test_unqualified_external_reference_fails_anywhere_in_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            package = self.make_package(skills_root, "alpha-skill")
            self.make_package(skills_root, "beta-skill")
            references = package / "references"
            references.mkdir()
            (references / "method.md").write_text(
                "Use $beta-skill for the next step.\n", encoding="utf-8"
            )

            report = validator.validate_packages(skills_root)

        self.assertFalse(report.ok)
        self.assertEqual(report.findings[0].code, "external-skill-reference")

    def test_availability_qualified_external_reference_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root,
                "alpha-skill",
                body="Use $beta-skill when it is available in the current runtime.",
            )

            report = validator.validate_packages(skills_root)

        self.assertTrue(report.ok)
        self.assertEqual(report.optional_reference_count, 1)
        self.assertEqual(len(report.external_references), 1)
        self.assertEqual(
            report.external_references[0].code, "optional-skill-reference"
        )

    def test_availability_qualification_must_share_the_reference_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root,
                "alpha-skill",
                body="When an evaluator is available:\n\nUse $beta-skill.",
            )

            report = validator.validate_packages(skills_root)

        self.assertFalse(report.ok)
        self.assertEqual(report.findings[0].code, "external-skill-reference")

    def test_cli_lists_allowed_external_references_for_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root,
                "alpha-skill",
                body="Use $beta-skill when it is available in the current runtime.",
            )
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = validator.main(
                    ["--skills-root", str(skills_root)]
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("REVIEW:", stdout.getvalue())
        self.assertIn("$beta-skill", stdout.getvalue())

    def test_explicit_bundle_contract_allows_external_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(
                skills_root, "alpha-skill", body="Use $beta-skill for evaluation."
            )
            self.make_package(skills_root, "beta-skill")
            (skills_root / "skill-bundles.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "bundles": {"paired-review": ["alpha-skill", "beta-skill"]},
                    }
                ),
                encoding="utf-8",
            )

            report = validator.validate_packages(skills_root)

        self.assertTrue(report.ok)
        self.assertEqual(report.bundled_reference_count, 1)
        self.assertEqual(len(report.external_references), 1)
        self.assertEqual(
            report.external_references[0].code, "bundled-skill-reference"
        )

    def test_bundle_contract_rejects_unknown_packages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            self.make_package(skills_root, "alpha-skill")
            (skills_root / "skill-bundles.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "bundles": {"paired-review": ["alpha-skill", "missing-skill"]},
                    }
                ),
                encoding="utf-8",
            )

            report = validator.validate_packages(skills_root)

        self.assertFalse(report.ok)
        self.assertIn("bundle-contract", {finding.code for finding in report.findings})


if __name__ == "__main__":
    unittest.main()
