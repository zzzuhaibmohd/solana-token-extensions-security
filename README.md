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

A professional, evidence-first multi-agent auditor for Solana programs and client code that integrates SPL Token-2022. The skill combines eight fixed specialists, centralized semantic deduplication, exhaustive pattern coverage, and fresh isolated verification for every candidate.

> ⚠️ **AI-Generated Security Review:** This report was produced by an AI-assisted multi-agent system and may contain mistakes, omissions, false positives, and false negatives. It does not prove the absence of vulnerabilities and must not be treated as a substitute for an independent manual security audit. A qualified security professional should manually review the code before production deployment or before the system handles valuable assets.

## Install and invoke

Place this directory at `~/.codex/skills/solana-token-extensions-security`, then invoke:

```text
$solana-token-extensions-security audit this repository
$solana-token-extensions-security review programs/vault and clients/token.ts
```

The invocation name remains stable for compatibility. Every completed in-scope audit writes:

```text
slot_zero_token_extensions_report_YYYYMMDD_HHMMSS.md
```

## Scope

Primary scope includes Anchor/native Solana Rust and Token-2022-relevant TypeScript or JavaScript clients, SDKs, account resolvers, ATA builders, and instruction constructors. Manifests, IDLs, program IDs, dependency versions, and configuration are peripheral evidence. Tests support reasoning but are not treated as audited production code.

## Eight-role architecture

| Role | Security surface |
|---|---|
| 1 | Token-program policy, account identity, mint/owner/ATA binding |
| 2 | Transfer fees, rounding, raw-balance accounting, amount conversions |
| 3 | Transfer hooks, extra-account metadata, dynamic accounts, CPI trust |
| 4 | Delegates, custody, pause/freeze, authorities, permissioned burn |
| 5 | Initialization, sizing, rent, reallocation, closure, mint provenance |
| 6 | Metadata, groups, pointers, WSOL, program IDs, interfaces, version drift |
| 7 | Confidential transfer and mint/burn, proofs, cryptographic key binding |
| 8 | Cross-flow asymmetry, bridges, alternate movement, complete coverage sweep |

All roles finish before candidates are deduplicated. Each distinct candidate then goes to a fresh isolated verifier that must prove attack execution, reachability, an unprivileged trigger, and material impact. If fresh verification is unavailable, the audit fails closed and emits no partial report.

## Pattern categories

The stable catalog is split into eight maintained categories: identity/program policy; fees and amounts; hooks and CPI; authorities and controls; lifecycle and sizing; metadata and interfaces; confidential state and proofs; and cross-flow parity. Every pattern has a unique `T22-*` ID, and the coverage role must classify every ID.

Dedicated v2 coverage includes Pausable behavior, Permissioned Burn, Scaled UI Amount, Confidential Mint/Burn proof freshness, ElGamal/auditor/registry binding, and deployed-program/SDK/client feature-version drift.

## Report contents

Each report includes the Slot Zero Security banner and disclaimer, engagement summary, audited scope and reviewed files, findings summary, confirmed findings, manual-review leads, limitations, and the manual-audit footer. Extension detection, full pattern coverage, candidate accounting, and agent/verifier provenance remain mandatory internal controls but are intentionally omitted from the client-facing report.

Findings use Critical/High/Medium/Low severity and 1–100 confidence. Findings below 80 confidence contain no prescriptive patch diff and require manual confirmation. Leads are deliberately unscored and contain no fix.

## Limitations

The skill cannot prove the absence of vulnerabilities, validate unknown production configuration without evidence, or replace deployment review, testing, monitoring, and human judgment. It will not continue with inline self-verification when a fresh isolated verifier is unavailable.

## Official references

- [Token extensions overview](https://solana.com/docs/tokens/extensions)
- [Token-2022 extension modules](https://github.com/solana-program/token-2022/blob/main/program/src/extension/mod.rs)
- [Scaled UI Amount interface](https://github.com/solana-program/token-2022/blob/main/interface/src/extension/scaled_ui_amount/mod.rs)
- [Permissioned Burn tracking issue](https://github.com/solana-program/token-2022/issues/772)
- [Confidential mint/burn proof freshness](https://github.com/solana-program/token-2022/issues/126)

For an independent Solana security engagement, visit [Slot Zero Security](https://slotzerosecurity.com/).

> AI analysis cannot guarantee security. Always combine this report with an independent manual audit, testing, monitoring, and an appropriate bug bounty program. Learn more at [Slot Zero Security](https://slotzerosecurity.com/).
