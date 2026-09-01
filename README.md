<pre>
███████╗██╗      ██████╗ ████████╗    ███████╗███████╗██████╗  ██████╗
██╔════╝██║     ██╔═══██╗╚══██╔══╝    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
███████╗██║     ██║   ██║   ██║          ███╔╝ █████╗  ██████╔╝██║   ██║
╚════██║██║     ██║   ██║   ██║         ███╔╝  ██╔══╝  ██╔══██╗██║   ██║
███████║███████╗╚██████╔╝   ██║        ███████╗███████╗██║  ██║╚██████╔╝
╚══════╝╚══════╝ ╚═════╝    ╚═╝        ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝

███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝
╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝
███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝

             SOLANA TOKEN EXTENSIONS SECURITY AUDITOR · v2
                    https://slotzerosecurity.com/
</pre>

# Solana Token Extensions Security Auditor v2

[![Version](https://img.shields.io/badge/version-2.0.0-0b7285.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)
[![Solana Token-2022](https://img.shields.io/badge/Solana-Token--2022-14f195.svg)](https://solana.com/docs/tokens/extensions)

An evidence-first, multi-agent security auditor for Solana programs and client code that integrate SPL Token-2022. Version 2.0.0 combines eight fixed specialists, a catalog of 61 stable security patterns, centralized semantic deduplication, and fresh isolated verification for every candidate.

The banner above is printed before discovery starts and placed at the beginning of every completed report.

> ⚠️ **AI-Generated Security Review:** This report was produced by an AI-assisted multi-agent system and may contain mistakes, omissions, false positives, and false negatives. It does not prove the absence of vulnerabilities and must not be treated as a substitute for an independent manual security audit. A qualified security professional should manually review the code before production deployment or before the system handles valuable assets.

## What it audits

Primary scope includes Anchor and native Solana Rust programs plus Token-2022-relevant TypeScript or JavaScript clients, SDKs, account resolvers, associated-token-account builders, and instruction constructors.

Manifests, IDLs, declared program IDs, lockfiles, dependency versions, feature flags, and deployment configuration are treated as peripheral evidence. Tests provide supporting context but are not treated as audited production code.

## Requirements and fail-closed behavior

A full audit requires repository filesystem access and the ability to launch fresh isolated subagents. The orchestrator never substitutes its own retained context for independent candidate verification.

- If discovery finds no Token-2022 surface, the scan stops without creating a report.
- If all eight role outputs cannot pass their schema gate, the scan stops without creating a partial report.
- If fresh isolated verification is unavailable, the scan cleans validated temporary artifacts and stops without presenting a partial report.

This capability gate is intentional. Host support for loading the skill alone does not imply support for completing its multi-agent audit workflow.

## Install

In Codex, use the bundled [`$skill-installer`](https://developers.openai.com/codex/skills) with the public repository:

```text
$skill-installer install the solana-token-extensions-security skill from https://github.com/SlotZeroSecurity/solana-token-extensions-security
```

The skill will be available on the next turn. Invoke it explicitly with its stable public name:

```text
$solana-token-extensions-security audit this repository
$solana-token-extensions-security review programs/vault and clients/token.ts
$solana-token-extensions-security scan this project for Token-2022 integration risks
```

## Runtime architecture

```text
Repository
    |
    v
Discovery and scope classification
    |-- no Token-2022 surface ----------------------> stop, no report
    v
Isolated source bundles
    v
R1  R2  R3  R4  R5  R6  R7  R8  (fixed specialist phase)
    v
Role-output schema gate
    |-- malformed or incomplete --------------------> stop, no partial report
    v
Central semantic deduplication and loss audit
    v
One fresh isolated verifier per candidate (V001, V002, ...)
    |-- isolated verification unavailable ----------> stop, no partial report
    v
61-pattern coverage finalization and candidate accounting
    v
Timestamped report
    v
Validated temporary-artifact cleanup
```

All eight specialists finish before deduplication. Candidates merge only when their handler, root cause, break condition, attack mechanism, material impact, remediation, and candidate kind are equivalent. Every surviving candidate then receives its own minimal evidence packet and fresh verifier, which evaluates attack execution, reachability, unprivileged trigger, and material impact.

## Eight specialist roles

| Role | Security surface |
|---|---|
| R1 | Token-program policy, account identity, mint/owner/ATA binding |
| R2 | Transfer fees, rounding, raw-balance accounting, amount conversions |
| R3 | Transfer hooks, extra-account metadata, dynamic accounts, CPI trust |
| R4 | Delegates, custody, pause/freeze, authorities, permissioned burn |
| R5 | Initialization, sizing, rent, reallocation, closure, mint provenance |
| R6 | Metadata, groups, pointers, WSOL, program IDs, interfaces, version drift |
| R7 | Confidential transfer and mint/burn, proofs, cryptographic key binding |
| R8 | Cross-flow asymmetry, bridges, alternate movement, complete coverage sweep |

## Pattern catalog

The catalog contains 61 permanent `T22-*` review anchors across eight categories. R1-R7 each own one category; R8 performs the complete cross-category coverage sweep and must classify every pattern ID.

| Category | Pattern count |
|---|---:|
| Identity and program policy | 6 |
| Fees and amounts | 8 |
| Hooks and CPI | 8 |
| Authorities and controls | 8 |
| Lifecycle and sizing | 8 |
| Metadata and interfaces | 8 |
| Confidential state and proofs | 7 |
| Cross-flow parity | 8 |
| **Total** | **61** |

Dedicated v2 coverage includes Pausable behavior, Permissioned Burn, Scaled UI Amount, Confidential Mint/Burn proof freshness, ElGamal/auditor/registry binding, and deployed-program/SDK/client feature-version drift.

## Reports

Every completed in-scope audit writes a report to the audited project root:

```text
slot_zero_token_extensions_report_YYYYMMDD_HHMMSS.md
```

Reports contain the Slot Zero Security banner, engagement summary, audited scope, findings summary, confirmed findings, manual-review leads, limitations, and security disclaimers. Internal extension detection, complete pattern coverage, candidate disposition accounting, and agent/verifier provenance remain mandatory audit gates but are intentionally excluded from the client-facing report.

Confirmed findings use Critical/High/Medium/Low severity and integer confidence from 1-100. Findings below 80 confidence omit prescriptive patch diffs and require manual confirmation. Leads are unscored and contain no fix.

## Package layout

```text
solana-token-extensions-security/
|-- SKILL.md                    Skill entrypoint and audit contract
|-- VERSION                     Current release identity (2.0.0)
|-- agents/openai.yaml          Optional Codex/ChatGPT interface metadata
|-- references/
|   |-- orchestration.md        Discovery through cleanup workflow
|   |-- shared-rules.md         Trust boundary and candidate schemas
|   |-- judging.md              Verification gates
|   |-- severity.md             Impact and likelihood scoring
|   |-- verification.md         Fresh-verifier verdict contract
|   |-- pattern-index.md        Stable 61-pattern taxonomy
|   |-- roles/                  Eight specialist prompts
|   |-- patterns/               Eight pattern-category catalogs
|   `-- report-template.md      Required client-facing report format
`-- scripts/
    |-- discover_scope.py       Deterministic scope discovery helper
    |-- test_discovery.py       Discovery behavior tests
    `-- validate_skill.py       Package and architecture validator
```

## Validate locally

The helper scripts use only the Python standard library:

```bash
python3 scripts/validate_skill.py
python3 scripts/test_discovery.py
```

The validator checks the fixed role and category counts, 61-pattern catalog, stable identifiers, v2 branding, report contract, metadata, and local Markdown references. The discovery tests cover Rust source, Token-2022 clients, supporting tests, peripheral evidence, and excluded directories.

## Limitations

The skill cannot prove the absence of vulnerabilities, establish unknown production configuration without evidence, or replace deployment review, testing, monitoring, and human judgment. Results depend on the supplied repository state, reachable local evidence, model behavior, and the host's ability to provide genuinely isolated verifier contexts.

The workflow does not modify audited source, tests, configuration, or dependencies, and it does not implement finding fixes unless separately requested after report review.

## Feedback

Feedback is welcome. Reports of false positives or false negatives, proposed Token-2022 patterns, portability observations, documentation corrections, and methodology suggestions all help improve the auditor while keeping its evidence and verification standards explicit.

## Official references

- [Token extensions overview](https://solana.com/docs/tokens/extensions)
- [Token-2022 extension modules](https://github.com/solana-program/token-2022/blob/main/program/src/extension/mod.rs)
- [Scaled UI Amount interface](https://github.com/solana-program/token-2022/blob/main/interface/src/extension/scaled_ui_amount/mod.rs)
- [Permissioned Burn tracking issue](https://github.com/solana-program/token-2022/issues/772)
- [Confidential mint/burn proof freshness](https://github.com/solana-program/token-2022/issues/126)

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Slot Zero Security.

For an independent Solana security engagement, visit [Slot Zero Security](https://slotzerosecurity.com/).

> AI analysis cannot guarantee security. Always combine this report with an independent manual audit, testing, monitoring, and an appropriate bug bounty program. Learn more at [Slot Zero Security](https://slotzerosecurity.com/).
