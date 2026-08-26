# R1 — Identity and Program Policy

Review the complete source bundle and [01-identity-program-policy.md](../patterns/01-identity-program-policy.md).

Trace every accepted mint and token account through creation, validation, authority use, transfer, and close. Determine whether classic SPL Token, Token-2022, or both are supported deliberately. Verify token-program ownership, executable address, mint/account relationships, owner/delegate authority, ATA derivation with the token program ID, mixed-program CPI legs, and generic-account versus ATA-only policy. Inspect Rust constraints and relevant client builders together.

Do not report interface use by itself. Prove that a reachable path accepts the wrong program, mint, account, authority, or canonical address and causes material harm. Return only blocks from [shared-rules.md](../shared-rules.md) using `R1-###` IDs.
