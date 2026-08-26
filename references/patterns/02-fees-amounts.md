# Fees and Amount Patterns

## T22-AMT-001 — Nominal Credit Instead of Net Balance Delta

- **Root cause:** protocol credit uses requested transfer amount instead of observed receiver-side delta.
- **Break condition:** transfer fees or other supported behavior reduce credited/spendable tokens.
- **Impact:** insolvency, withdrawal failure, underpayment, or reserve drift.
- **Remediation:** reconcile balance deltas and book the net amount actually received.

## T22-AMT-002 — Fee Rounding or Inverse-Calculation Error

- **Root cause:** fee estimates, `calculate_fee`, inverse fee, and pre-fee calculations are treated as exact inverses.
- **Break condition:** boundary amounts or maximum fees produce one-unit or capped rounding differences.
- **Impact:** chronic accounting drift, underfunded payouts, or exploitable quote/settlement mismatch.
- **Remediation:** use the correct fee-aware primitive and assert expected fee and post-transfer balances.

## T22-AMT-003 — Withheld-Fee State Ignored

- **Root cause:** close, reporting, or settlement logic treats an account or mint as empty without considering withheld fees and harvesting.
- **Break condition:** fees remain in token accounts or are not synchronized to the mint.
- **Impact:** stuck closure, lost claimable value, or inaccurate reserve/fee accounting.
- **Remediation:** inspect withheld state and harvest/synchronize it before close or settlement.

## T22-AMT-004 — Epoch-Delayed Fee Configuration Drift

- **Root cause:** clients or programs assume fee updates are immediate or use stale schedule data.
- **Break condition:** the effective epoch fee differs from the quoted or authorized fee.
- **Impact:** unexpected user loss, failed exact-fee instructions, or broken pricing/accounting.
- **Remediation:** query the effective epoch schedule and bind transactions to an expected fee.

## T22-AMT-005 — Interest-Bearing UI Value Used as Principal

- **Root cause:** time-derived UI conversion is treated as raw balance, principal, oracle price, or protocol yield.
- **Break condition:** elapsed time or rate changes alter display amounts without changing raw tokens.
- **Impact:** incorrect collateral, rewards, limits, or settlement.
- **Remediation:** keep raw accounting authoritative and isolate display conversion from economic state.

## T22-AMT-006 — Scaled UI Multiplier Update Breaks Raw/UI Separation

- **Root cause:** stored authorization or accounting values use scaled UI amounts as if they were immutable raw units.
- **Break condition:** the multiplier changes between quote, approval, execution, or settlement.
- **Impact:** over/under-transfer, limit bypass, bad debt, or inconsistent client display.
- **Remediation:** store and authorize raw integer amounts; apply the current multiplier only at explicit UI boundaries.

## T22-AMT-007 — Scaled UI Floating-Point or Truncation Error

- **Root cause:** client or program conversions use lossy floating point, unchecked exponent ranges, or inconsistent rounding.
- **Break condition:** large, fractional, or boundary UI inputs convert differently across components.
- **Impact:** exploitable quote/transfer mismatch, dust loss, or limit bypass.
- **Remediation:** use bounded deterministic conversion, explicit rounding direction, and cross-language boundary tests.

## T22-AMT-008 — Unchecked Transfer Amount or Decimals

- **Root cause:** plain transfer or client serialization omits mint-aware decimals and expected fee data.
- **Break condition:** a substituted mint or stale client assumption changes amount interpretation.
- **Impact:** wrong-value transfer, failed settlement, or asset confusion.
- **Remediation:** use mint-aware checked instructions and validate decimals, program ID, and expected fee.
