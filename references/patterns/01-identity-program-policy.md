# Identity and Program Policy Patterns

## T22-ID-001 — Ambiguous Token-2022 Support Policy

- **Root cause:** interface types or generic client helpers accept both token programs without an explicit allow/deny policy.
- **Break condition:** an asset from the unintended program family reaches a path whose assumptions were written for the other family.
- **Impact:** wrong-program CPI, unsupported extension behavior, fund lock, or accounting/security-policy bypass.
- **Remediation:** bind every supported mint and token account to an explicit token-program policy and test both families separately.

## T22-ID-002 — Mint, Owner, and Authority Binding Failure

- **Root cause:** token accounts are not bound independently to the expected mint, token owner, and signing owner or approved delegate.
- **Break condition:** an attacker substitutes a valid account or authority with a different semantic role.
- **Impact:** misrouted assets, unauthorized transfer/burn, or cross-instance accounting corruption.
- **Remediation:** validate token-program owner, mint, token-account owner, delegate, and authority relationships separately.

## T22-ID-003 — Program-Unaware ATA Derivation

- **Root cause:** ATA derivation omits the token program ID or uses a classic-SPL default.
- **Break condition:** a Token-2022 flow compares against or creates the wrong canonical ATA.
- **Impact:** blocked deposits/claims/settlement or routing to an unintended account.
- **Remediation:** derive ATAs with the intended token program ID in program and client code.

## T22-ID-004 — Mixed Token-Program CPI Leg Reuse

- **Root cause:** a multi-asset instruction reuses one token-program account across CPI legs.
- **Break condition:** the legs operate on assets owned by different token programs.
- **Impact:** durable integration denial, wrong executable target, or stranded settlement.
- **Remediation:** bind and pass the correct token-program account for every CPI leg, or enforce one family for all legs.

## T22-ID-005 — Base Layout Accepted Without Extension Inspection

- **Root cause:** classic-compatible base deserialization is treated as evidence that Token-2022 extensions are harmless.
- **Break condition:** an accepted mint/account carries transfer, authority, closure, or confidentiality semantics the protocol never modeled.
- **Impact:** violated custody, transferability, accounting, or lifecycle assumptions.
- **Remediation:** parse extension state and apply an explicit supported-extension policy before use.

## T22-ID-006 — ATA-Only and Generic-Account Policy Mismatch

- **Root cause:** some paths allow generic token accounts while others assume all accounts are canonical ATAs.
- **Break condition:** an attacker or legitimate user supplies a valid non-ATA account to an inconsistent lifecycle.
- **Impact:** bypassed identity assumptions or permanently blocked exit/close flows.
- **Remediation:** choose ATA-only or generic-account support and enforce the same policy across every path.
