#!/usr/bin/env python3
"""Validate repository skill package names and cross-skill references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\n(?P<body>.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL
)
SKILL_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_$])\$(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)\b"
)
AVAILABILITY_RE = re.compile(
    r"(?:"
    r"\b(?:if|when|where)\b[^\n]{0,160}"
    r"\b(?:available|installed|configured|enabled|exposed|provided|provides|includes)\b"
    r"|\b(?:available|installed|configured|enabled|exposed|provided)\b"
    r"[^\n]{0,160}\b(?:if|when|where)\b"
    r"|사용\s*가능(?:한\s*경우|하면)"
    r"|설치(?:된\s*경우|되어\s*있으면)"
    r"|런타임(?:에서|이)\s*제공(?:되는\s*경우|하면)"
    r")",
    re.IGNORECASE,
)
IGNORED_PARTS = {".git", "__pycache__"}
BUNDLE_SCHEMA_VERSION = 1


@dataclass(frozen=True, order=True)
class Finding:
    path: Path
    line: int
    column: int
    code: str
    message: str

    def render(self, root: Path) -> str:
        try:
            display_path = self.path.resolve().relative_to(root.resolve())
        except ValueError:
            display_path = self.path
        return (
            f"{display_path}:{self.line}:{self.column}: "
            f"{self.code}: {self.message}"
        )


@dataclass
class ValidationReport:
    package_count: int = 0
    self_reference_count: int = 0
    optional_reference_count: int = 0
    bundled_reference_count: int = 0
    external_references: list[Finding] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def external_reference_count(self) -> int:
        return self.optional_reference_count + self.bundled_reference_count

    @property
    def ok(self) -> bool:
        return not self.findings


def package_directories(skills_root: Path) -> list[Path]:
    if not skills_root.is_dir():
        return []
    return sorted(
        child
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    )


def frontmatter_name(skill_md: Path) -> tuple[str | None, list[Finding]]:
    findings: list[Finding] = []
    try:
        content = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeError) as error:
        return None, [
            Finding(skill_md, 1, 1, "package-read", f"cannot read SKILL.md: {error}")
        ]
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, [
            Finding(
                skill_md,
                1,
                1,
                "frontmatter",
                "SKILL.md must start with a complete YAML frontmatter block",
            )
        ]
    name_lines = re.findall(r"(?m)^name:[ \t]*(.*?)[ \t]*$", match.group("body"))
    if len(name_lines) != 1:
        return None, [
            Finding(
                skill_md,
                2,
                1,
                "package-name",
                "frontmatter must contain exactly one scalar name",
            )
        ]
    raw_name = name_lines[0].strip()
    if len(raw_name) >= 2 and raw_name[0] == raw_name[-1] and raw_name[0] in "\"'":
        raw_name = raw_name[1:-1]
    if not NAME_RE.fullmatch(raw_name):
        findings.append(
            Finding(
                skill_md,
                2,
                1,
                "package-name",
                "frontmatter name must use lowercase hyphen-case",
            )
        )
        return None, findings
    return raw_name, findings


def text_files(package: Path) -> Iterable[tuple[Path, str]]:
    for path in sorted(package.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in data:
            continue
        try:
            yield path, data.decode("utf-8")
        except UnicodeDecodeError:
            continue


def reference_location(text: str, offset: int) -> tuple[int, int, str]:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end < 0:
        line_end = len(text)
    line = text.count("\n", 0, offset) + 1
    column = offset - line_start + 1
    return line, column, text[line_start:line_end]


def load_bundle_memberships(
    contract_path: Path, package_names: set[str]
) -> tuple[dict[str, set[str]], list[Finding]]:
    memberships: dict[str, set[str]] = defaultdict(set)
    if not contract_path.exists():
        return memberships, []
    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
    except OSError as error:
        return memberships, [
            Finding(
                contract_path,
                1,
                1,
                "bundle-contract",
                f"cannot read bundle contract: {error}",
            )
        ]
    except json.JSONDecodeError as error:
        return memberships, [
            Finding(
                contract_path,
                error.lineno,
                error.colno,
                "bundle-contract",
                "bundle contract is not valid JSON",
            )
        ]
    findings: list[Finding] = []
    if not isinstance(raw, Mapping) or set(raw) != {"schema_version", "bundles"}:
        return memberships, [
            Finding(
                contract_path,
                1,
                1,
                "bundle-contract",
                "contract must contain only schema_version and bundles",
            )
        ]
    if raw["schema_version"] != BUNDLE_SCHEMA_VERSION:
        findings.append(
            Finding(
                contract_path,
                1,
                1,
                "bundle-contract",
                f"schema_version must be {BUNDLE_SCHEMA_VERSION}",
            )
        )
    bundles = raw["bundles"]
    if not isinstance(bundles, Mapping):
        findings.append(
            Finding(
                contract_path,
                1,
                1,
                "bundle-contract",
                "bundles must be an object of bundle names to package arrays",
            )
        )
        return memberships, findings
    for bundle_name, members in bundles.items():
        if not isinstance(bundle_name, str) or not NAME_RE.fullmatch(bundle_name):
            findings.append(
                Finding(
                    contract_path,
                    1,
                    1,
                    "bundle-contract",
                    "bundle names must use lowercase hyphen-case",
                )
            )
            continue
        if (
            not isinstance(members, list)
            or len(members) < 2
            or not all(isinstance(member, str) for member in members)
            or len(members) != len(set(members))
        ):
            findings.append(
                Finding(
                    contract_path,
                    1,
                    1,
                    "bundle-contract",
                    f"bundle {bundle_name!r} must contain at least two unique "
                    "package names",
                )
            )
            continue
        unknown = sorted(set(members) - package_names)
        if unknown:
            findings.append(
                Finding(
                    contract_path,
                    1,
                    1,
                    "bundle-contract",
                    f"bundle {bundle_name!r} names unknown packages: "
                    f"{', '.join(unknown)}",
                )
            )
            continue
        for member in members:
            memberships[member].add(bundle_name)
    return memberships, findings


def share_bundle(
    source: str, target: str, memberships: Mapping[str, set[str]]
) -> bool:
    return bool(memberships.get(source, set()) & memberships.get(target, set()))


def resolve_requested_packages(
    skills_root: Path, requested: Sequence[str]
) -> tuple[list[Path], list[Finding]]:
    if not requested:
        packages = package_directories(skills_root)
        if packages:
            return packages, []
        return [], [
            Finding(
                skills_root,
                1,
                1,
                "package-discovery",
                "no skill packages with SKILL.md were found",
            )
        ]
    packages: list[Path] = []
    findings: list[Finding] = []
    seen: set[Path] = set()
    for value in requested:
        candidate = Path(value)
        if not candidate.is_absolute() and not candidate.exists():
            candidate = skills_root / value
        candidate = candidate.resolve()
        if not (candidate / "SKILL.md").is_file():
            findings.append(
                Finding(
                    candidate,
                    1,
                    1,
                    "package-discovery",
                    "requested package does not contain SKILL.md",
                )
            )
            continue
        if candidate not in seen:
            packages.append(candidate)
            seen.add(candidate)
    return sorted(packages), findings


def validate_packages(
    skills_root: Path,
    requested: Sequence[str] = (),
    bundle_contract: Path | None = None,
) -> ValidationReport:
    skills_root = skills_root.resolve()
    packages, discovery_findings = resolve_requested_packages(skills_root, requested)
    report = ValidationReport(package_count=len(packages))
    report.findings.extend(discovery_findings)

    all_packages = package_directories(skills_root)
    package_names = {package.name for package in all_packages}
    contract_path = (
        bundle_contract.resolve()
        if bundle_contract is not None
        else skills_root / "skill-bundles.json"
    )
    memberships, bundle_findings = load_bundle_memberships(
        contract_path, package_names
    )
    report.findings.extend(bundle_findings)

    declared_names: dict[str, Path] = {}
    for package in packages:
        skill_md = package / "SKILL.md"
        declared_name, name_findings = frontmatter_name(skill_md)
        report.findings.extend(name_findings)
        package_name = declared_name or package.name
        if declared_name is not None and declared_name != package.name:
            report.findings.append(
                Finding(
                    skill_md,
                    2,
                    1,
                    "package-name",
                    f"frontmatter name {declared_name!r} must match directory "
                    f"{package.name!r}",
                )
            )
        if declared_name is not None:
            prior = declared_names.get(declared_name)
            if prior is not None:
                report.findings.append(
                    Finding(
                        skill_md,
                        2,
                        1,
                        "package-name",
                        f"frontmatter name duplicates {prior}",
                    )
                )
            else:
                declared_names[declared_name] = package

        for path, text in text_files(package):
            for match in SKILL_REFERENCE_RE.finditer(text):
                target = match.group("name")
                if target == package_name:
                    report.self_reference_count += 1
                    continue
                line, column, line_text = reference_location(text, match.start())
                if AVAILABILITY_RE.search(line_text):
                    report.optional_reference_count += 1
                    report.external_references.append(
                        Finding(
                            path,
                            line,
                            column,
                            "optional-skill-reference",
                            f"${target} is availability-qualified and requires review",
                        )
                    )
                    continue
                if share_bundle(package_name, target, memberships):
                    report.bundled_reference_count += 1
                    report.external_references.append(
                        Finding(
                            path,
                            line,
                            column,
                            "bundled-skill-reference",
                            f"${target} is covered by an explicit bundle contract",
                        )
                    )
                    continue
                report.findings.append(
                    Finding(
                        path,
                        line,
                        column,
                        "external-skill-reference",
                        f"${target} must be availability-qualified on the same line "
                        "or covered by skills/skill-bundles.json",
                    )
                )

    report.findings.sort()
    report.external_references.sort()
    return report


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description=(
            "Validate skill package names and reject undeclared cross-skill references"
        )
    )
    repository_root = Path(__file__).resolve().parents[1]
    root.add_argument(
        "packages",
        nargs="*",
        help=(
            "package names under --skills-root or explicit package paths; "
            "default: all"
        ),
    )
    root.add_argument(
        "--skills-root",
        type=Path,
        default=repository_root / "skills",
        help="directory containing canonical skill packages",
    )
    root.add_argument(
        "--bundle-contract",
        type=Path,
        help=(
            "optional explicit bundle contract; default: "
            "<skills-root>/skill-bundles.json"
        ),
    )
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    report = validate_packages(
        args.skills_root, args.packages, args.bundle_contract
    )
    repository_root = Path(__file__).resolve().parents[1]
    for reference in report.external_references:
        print(f"REVIEW: {reference.render(repository_root)}")
    if report.findings:
        for finding in report.findings:
            print(finding.render(repository_root), file=sys.stderr)
        print(
            f"FAIL: {len(report.findings)} finding(s) across "
            f"{report.package_count} package(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"PASS: {report.package_count} package(s), "
        f"{report.self_reference_count} self reference(s), "
        f"{report.optional_reference_count} optional external reference(s), "
        f"{report.bundled_reference_count} bundled external reference(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
