#!/usr/bin/env python3
"""Validate Slot Zero Security Token Extensions Auditor v2 invariants."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


EXACT_DISCLAIMER = (
    "⚠️ **AI-Generated Security Review:** This report was produced by an AI-assisted multi-agent system "
    "and may contain mistakes, omissions, false positives, and false negatives. It does not prove the absence "
    "of vulnerabilities and must not be treated as a substitute for an independent manual security audit. "
    "A qualified security professional should manually review the code before production deployment or before "
    "the system handles valuable assets."
)
EXACT_FOOTER = (
    "AI analysis cannot guarantee security. Always combine this report with an independent manual audit, testing, "
    "monitoring, and an appropriate bug bounty program. Learn more at [Slot Zero Security](https://slotzerosecurity.com/)."
)
STALE = (
    "Solana Token-2022 Security Review",
    "SLOTZERO SCAN",
    "Solana adversarial review",
    "finding-templates.md",
    "token-2022-patterns.md",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    required = [
        root / "SKILL.md", root / "README.md", root / "VERSION", root / "agents/openai.yaml",
        root / "references/orchestration.md", root / "references/shared-rules.md",
        root / "references/judging.md", root / "references/severity.md",
        root / "references/verification.md", root / "references/report-template.md",
        root / "references/pattern-index.md", root / "references/legacy-map.md",
    ]
    for path in required:
        if not path.is_file():
            fail(errors, f"missing required file: {path.relative_to(root)}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if (root / "VERSION").read_text().strip() != "2.0.0":
        fail(errors, "VERSION must be 2.0.0")

    markdown = {path: path.read_text(encoding="utf-8") for path in root.rglob("*.md")}
    yaml_text = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    all_text = "\n".join(markdown.values()) + "\n" + yaml_text
    for stale in STALE:
        if stale in all_text:
            fail(errors, f"stale branding/reference found: {stale}")

    for path in (root / "SKILL.md", root / "README.md", root / "references/report-template.md"):
        text = markdown[path]
        for token in ("Slot Zero Security", "v2", "https://slotzerosecurity.com/"):
            if token not in text:
                fail(errors, f"{path.relative_to(root)} missing {token}")

    for path in (root / "README.md", root / "references/report-template.md"):
        text = markdown[path]
        if EXACT_DISCLAIMER not in text:
            fail(errors, f"{path.relative_to(root)} missing exact AI disclaimer")
        if EXACT_FOOTER not in text:
            fail(errors, f"{path.relative_to(root)} missing exact footer")

    roles = sorted((root / "references/roles").glob("[0-9][0-9]-*.md"))
    if len(roles) != 8:
        fail(errors, f"expected exactly 8 role files, found {len(roles)}")
    expected_roles = {f"R{i}" for i in range(1, 9)}
    found_roles = set()
    for path in roles:
        match = re.search(r"^# (R[1-8]) —", path.read_text(), re.MULTILINE)
        if not match:
            fail(errors, f"role heading invalid: {path.relative_to(root)}")
        else:
            found_roles.add(match.group(1))
    if found_roles != expected_roles:
        fail(errors, f"role IDs mismatch: {sorted(found_roles)}")

    orchestration = markdown[root / "references/orchestration.md"]
    for invariant in (
        "R1–R7 may cite only IDs from their assigned category",
        "Assign immutable contiguous verifier IDs `V001`",
        "stop without a report",
        "Do not present a partial report",
    ):
        if invariant.lower() not in orchestration.lower():
            fail(errors, f"orchestration missing invariant: {invariant}")
    if "verifier_id: V001" not in markdown[root / "references/verification.md"]:
        fail(errors, "verification schema missing verifier_id")

    report_template = markdown[root / "references/report-template.md"]
    skill_text = markdown[root / "SKILL.md"]
    expected_report_name = "slot_zero_token_extensions_report_YYYYMMDD_HHMMSS.md"
    if expected_report_name not in skill_text or expected_report_name not in orchestration or expected_report_name not in report_template:
        fail(errors, "short report filename is not consistent across runtime and template")
    forbidden_report_sections = (
        "## Detected Token-2022 surface",
        "## Pattern coverage",
        "## Provenance and completeness",
    )
    for heading in forbidden_report_sections:
        if heading in report_template:
            fail(errors, f"client-facing report still contains noisy section: {heading}")
    for internal_field in ("**Pattern IDs:**", "**Source candidates:**", "| Completed roles |"):
        if internal_field in report_template:
            fail(errors, f"client-facing report still exposes internal field: {internal_field}")

    pattern_files = sorted((root / "references/patterns").glob("[0-9][0-9]-*.md"))
    if len(pattern_files) != 8:
        fail(errors, f"expected exactly 8 pattern files, found {len(pattern_files)}")
    canonical: list[str] = []
    for path in pattern_files:
        text = path.read_text()
        canonical.extend(re.findall(r"^## (T22-[A-Z]+-[0-9]{3}) —", text, re.MULTILINE))
        headings = re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE)
        dupes = [heading for heading, count in Counter(headings).items() if count > 1]
        if dupes:
            fail(errors, f"duplicate headings in {path.relative_to(root)}: {dupes}")
    canonical_counts = Counter(canonical)
    duplicates = sorted(key for key, count in canonical_counts.items() if count != 1)
    if duplicates:
        fail(errors, f"duplicate canonical pattern IDs: {duplicates}")
    if len(canonical) != 61:
        fail(errors, f"expected 61 canonical patterns, found {len(canonical)}")

    index_text = markdown[root / "references/pattern-index.md"]
    indexed = set(re.findall(r"T22-[A-Z]+-[0-9]{3}", index_text))
    if indexed != set(canonical):
        fail(errors, f"pattern index mismatch; missing={sorted(set(canonical)-indexed)}, extra={sorted(indexed-set(canonical))}")

    required_new = {
        "T22-AUTH-003", "T22-AUTH-004", "T22-AMT-006", "T22-AMT-007",
        "T22-CONF-003", "T22-CONF-004", "T22-META-008",
    }
    if not required_new <= set(canonical):
        fail(errors, f"missing v2 patterns: {sorted(required_new-set(canonical))}")

    legacy_text = markdown[root / "references/legacy-map.md"]
    legacy_ids = set(re.findall(r"T22-[A-Z]+-[0-9]{3}", legacy_text))
    if not legacy_ids <= set(canonical):
        fail(errors, f"legacy map references unknown IDs: {sorted(legacy_ids-set(canonical))}")

    link_re = re.compile(r"\[[^]]+\]\(([^)]+\.md)\)")
    for path, text in markdown.items():
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_file():
                fail(errors, f"broken local link in {path.relative_to(root)}: {target}")

    skill = markdown[root / "SKILL.md"]
    if not skill.startswith("---\nname: solana-token-extensions-security\n"):
        fail(errors, "SKILL.md frontmatter name invalid")
    if "description:" not in skill.split("---", 2)[1]:
        fail(errors, "SKILL.md missing description")
    if "$solana-token-extensions-security" not in yaml_text:
        fail(errors, "metadata default_prompt missing invocation")
    for token in (
        "Slot Zero Security",
        "Solana Token Extensions Security Auditor v2",
    ):
        if token not in yaml_text:
            fail(errors, f"metadata missing consistent identity: {token}")

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        print("\n".join(f"- {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"VALIDATION PASSED: 8 roles, 8 categories, {len(canonical)} unique patterns, v2 branding consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
