# R2 — Fees, Balances, and Amounts

Review the complete source bundle and [02-fees-amounts.md](../patterns/02-fees-amounts.md).

Trace asset ingress, internal credit, settlement, and egress using raw token-account balances. Test transfer-fee net amounts, withheld fees, epoch-delayed configuration, fee rounding and inverse calculations, interest-bearing conversions, Scaled UI Amount multipliers, raw/UI separation, floating-point boundaries, truncation, decimals, and client serialization. Compare every recorded amount with the balance delta that makes it economically true.

Distinguish display-only errors from security-relevant authorization, accounting, pricing, or payout errors. Return only blocks from [shared-rules.md](../shared-rules.md) using `R2-###` IDs.
