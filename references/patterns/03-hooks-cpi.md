# Hook and CPI Patterns

## T22-HOOK-001 — Missing Extra-Account Forwarding

- **Root cause:** a wrapper or client drops hook-required remaining accounts.
- **Break condition:** a supported mint resolves one or more extra account metas.
- **Impact:** critical flow denial or incomplete policy execution.
- **Remediation:** resolve and forward the complete ordered account set end to end.

## T22-HOOK-002 — Wrong Instruction Namespace for Extra Metas

- **Root cause:** one action reuses another action's PDA seed, discriminator, resolver, or validation account.
- **Break condition:** transfer/freeze/thaw or paired actions require distinct namespaces.
- **Impact:** one-sided policy failure or unusable permissionless flow.
- **Remediation:** derive and test each instruction-specific metadata namespace consistently on chain and in clients.

## T22-HOOK-003 — Dynamic CPI Account Role Not Bound

- **Root cause:** positional remaining accounts are checked only for length or executability, not semantic identity.
- **Break condition:** caller-selected state, mint, authority, or event accounts reach a privileged CPI role.
- **Impact:** cross-instance routing, privilege redirection, or policy bypass.
- **Remediation:** derive deterministic roles locally and bind every remaining role to validated state.

## T22-HOOK-004 — Hook or Gate Program Identity Not Bound

- **Root cause:** executable status substitutes for checking the authoritative program address.
- **Break condition:** a caller chooses an executable hook/gate while signer or mutable privileges are forwarded.
- **Impact:** fake-policy execution, signer exposure, or privileged state manipulation.
- **Remediation:** bind program ID to mint extension, trusted configuration, or imported declared ID and minimize privileges.

## T22-HOOK-005 — Wrapper-Only Policy Enforcement

- **Root cause:** pause, allowlist, compliance, or rate limits exist only in a convenience wrapper.
- **Break condition:** a directly callable downstream entrypoint reaches the same protected transition.
- **Impact:** policy bypass or unauthorized value movement.
- **Remediation:** enforce the invariant at the lowest unavoidable state-transition boundary or authenticate the wrapper.

## T22-HOOK-006 — Copied Hook Schema or Discriminator Drift

- **Root cause:** local constants, layouts, seeds, or discriminators are not tied to the pinned dependency.
- **Break condition:** dependency or deployed integration changes while copied code still compiles.
- **Impact:** fail-open parsing, fund lock, or durable supported-flow denial.
- **Remediation:** import upstream types/constants or assert compatibility against the pinned representation.

## T22-HOOK-007 — Required Memo Sequencing Omitted

- **Root cause:** transfer construction does not prepend a required memo or forwards transactions in the wrong order.
- **Break condition:** destination account enables required memo on incoming transfers.
- **Impact:** recipient-specific denial of deposit, payout, or settlement.
- **Remediation:** detect memo requirements and construct atomic memo-then-transfer sequences.

## T22-HOOK-008 — CPI Guard and Delegate Flow Mismatch

- **Root cause:** a protocol assumes owner authority remains usable during CPI or omits the required approval/delegate model.
- **Break condition:** token account enables CPI Guard.
- **Impact:** unusable custody, transfer, liquidation, or recovery flow.
- **Remediation:** design explicit delegate approvals and verify supported CPI behavior across all lifecycle paths.
