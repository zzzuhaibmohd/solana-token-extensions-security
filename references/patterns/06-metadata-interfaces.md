# Metadata and Interface Patterns

## T22-META-001 — Metadata Pointer and Data Are Not Mutually Bound

- **Root cause:** external or internal metadata is trusted without verifying the mint's authoritative pointer and reverse mint relation.
- **Break condition:** an attacker supplies separate metadata that names a legitimate mint.
- **Impact:** authorization, pricing, identity, or asset-class spoofing.
- **Remediation:** verify pointer authority, target address, owning program, and mutual mint binding.

## T22-META-002 — Group or Member Pointer Is Not Authoritative

- **Root cause:** group/member data is trusted by content or address alone rather than the mint's pointer relationships.
- **Break condition:** fake group or member accounts imitate a trusted collection.
- **Impact:** membership/eligibility bypass or asset misclassification.
- **Remediation:** validate group pointer, member pointer, member mint, group identity, and update authorities end to end.

## T22-META-003 — Unreferenced Extension Data Drives Security Decisions

- **Root cause:** clients or programs accept any plausible metadata/group account rather than the account selected by the mint.
- **Break condition:** attacker-created extension-adjacent data enters authorization, price, or routing logic.
- **Impact:** spoofed permissions, collateral identity, or settlement destination.
- **Remediation:** accept only authoritative pointer-selected state and bind all security decisions to it.

## T22-META-004 — SPL and Token-2022 WSOL Identity Confused

- **Root cause:** WSOL special-casing assumes one canonical mint across both token programs.
- **Break condition:** Token-2022 WSOL reaches a path intended for classic SPL WSOL, or vice versa.
- **Impact:** wrong unwrap behavior, pricing/routing error, or unsupported-asset lock.
- **Remediation:** bind WSOL identity to both the exact mint and token program; reject the unintended variant.

## T22-META-005 — Token Program ID Selected by Default

- **Root cause:** SDK helper, CPI builder, or client default silently selects classic SPL Token when Token-2022 is intended.
- **Break condition:** the program ID is omitted, stale, or user-selected inconsistently.
- **Impact:** wrong executable call, incorrect ATA, failed transfer, or asset confusion.
- **Remediation:** pass and validate the exact token program ID through every layer.

## T22-META-006 — Anchor Interface Selection Expands Support Accidentally

- **Root cause:** `token_interface` or generic types are used without implementing extension-aware behavior.
- **Break condition:** a Token-2022 mint passes type checks into classic-only logic.
- **Impact:** extension policy bypass, accounting error, or permanent flow denial.
- **Remediation:** use interface types only with explicit dual-program support; otherwise pin classic types and ownership.

## T22-META-007 — Local Interface Schema Drifts from Dependency

- **Root cause:** IDLs, discriminators, enums, seeds, or account layouts are copied instead of dependency-bound.
- **Break condition:** a crate or SDK upgrade changes the representation.
- **Impact:** fail-open decode, wrong PDA, fund lock, or durable integration denial.
- **Remediation:** import canonical definitions or enforce build/integration assertions against pinned versions.

## T22-META-008 — Deployed Program and Client Feature-Version Drift

- **Root cause:** the program, Rust crate, CLI, SDK, client resolver, or deployment assumes a Token-2022 feature not present—or behaves differently—in another layer's version.
- **Break condition:** feature rollout, extension tag, instruction shape, proof format, or account resolver differs across deployed and built components.
- **Impact:** malformed transactions, missing validation, fail-open compatibility shim, or critical-flow denial.
- **Remediation:** maintain an explicit compatibility matrix, pin versions/program IDs, and gate upgrades on end-to-end feature fixtures.
