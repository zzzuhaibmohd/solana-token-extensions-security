# Lifecycle and Sizing Patterns

## T22-LIFE-001 — Incomplete Extension Set Used for Mint Size

- **Root cause:** mint space is calculated before all conditional extensions are collected.
- **Break condition:** later initialization attempts to add an omitted extension.
- **Impact:** mint creation or required feature path fails permanently.
- **Remediation:** build the final extension set first, then calculate size and create the account.

## T22-LIFE-002 — Extension Dependency or Initialization Order Violation

- **Root cause:** initialization ignores dependency constraints or initializes the mint/base state too early.
- **Break condition:** combined extensions require prerequisite state, such as confidential transfer fee with transfer fee and confidential transfer.
- **Impact:** unusable mint, partial configuration, or permanently disabled feature.
- **Remediation:** validate the complete dependency graph and execute the canonical initialization order.

## T22-LIFE-003 — Static Token-Account Size or Rent Assumption

- **Root cause:** code hardcodes classic account length, rent, or RPC helpers that omit extensions.
- **Break condition:** required account extensions increase allocated size.
- **Impact:** account creation failure, underfunding, or blocked onboarding.
- **Remediation:** calculate size and rent from the actual extension set with program-aware helpers.

## T22-LIFE-004 — Unsafe Reallocation Authority or Rent Payer

- **Root cause:** reallocation accepts attacker-influenced extensions, lacks authority binding, or has no bounded payer policy.
- **Break condition:** a user or relayer expands an account or mandatory rent top-up cannot be funded.
- **Impact:** rent griefing, unauthorized extension state, or permanent account unusability.
- **Remediation:** authorize and bound extension additions, calculate delta rent, and define the payer explicitly.

## T22-LIFE-005 — Closure Ignores Extension State

- **Root cause:** closure checks only raw amount zero and ignores withheld fees, confidential balances, close authority, or extension-specific closability.
- **Break condition:** hidden or pending extension state remains.
- **Impact:** stuck close, lost value, or incorrect lifecycle completion.
- **Remediation:** use extension-aware closability checks and settle every residual state first.

## T22-LIFE-006 — Close-and-Reinitialize Breaks Mint Provenance

- **Root cause:** current mint address/state is treated as proof of historical identity.
- **Break condition:** a closeable zero-supply mint is closed and recreated with different extensions or authorities.
- **Impact:** allowlist/provenance bypass, incompatible legacy accounts, or changed custody policy.
- **Remediation:** require trusted mint provenance and never infer history from current extension state alone.

## T22-LIFE-007 — Immediate-Usability Assumption After Creation

- **Root cause:** a flow creates and consumes an account without checking required initialization, frozen, memo, or confidential state.
- **Break condition:** supported extensions require follow-up configuration before use.
- **Impact:** atomic transaction failure, trapped funds, or unusable keeper flow.
- **Remediation:** model the complete readiness state machine and verify readiness before asset movement.

## T22-LIFE-008 — Lifecycle Path Omits Extension Cleanup

- **Root cause:** exit, migration, emergency, or upgrade paths were designed for classic token state and omit extension cleanup/synchronization.
- **Break condition:** a supported extension leaves fees, keys, pointers, approvals, or policy state behind.
- **Impact:** stranded assets, stale privilege, or permanently blocked migration/closure.
- **Remediation:** enumerate extension state for every terminal path and make cleanup symmetric with initialization.
