# Cross-Flow Parity Patterns

## T22-FLOW-001 — Alternate Value Movement Bypasses Transfer Policy

- **Root cause:** transfer-hook, pause, fee, memo, or compliance policy is enforced only on ordinary transfer.
- **Break condition:** burn/remint, revoke/issue, close/recreate, wrap/unwrap, seizure, or bridge moves equivalent value.
- **Impact:** policy bypass or restricted value escapes its intended domain.
- **Remediation:** define policy over economic movement and enforce a shared validator before every equivalent transition.

## T22-FLOW-002 — Ingress and Egress Accounting Are Asymmetric

- **Root cause:** deposit books net/raw value differently from withdrawal, repayment, reward, or settlement.
- **Break condition:** fees, scaling, interest UI, or external balance mutation affects only one side.
- **Impact:** insolvency, unfair payout, or blocked exits.
- **Remediation:** express every path in one raw-balance accounting invariant and reconcile actual deltas.

## T22-FLOW-003 — Public Callee Bypasses Protected Wrapper

- **Root cause:** a wrapper applies policy but its state-changing callee is independently callable.
- **Break condition:** an unprivileged caller satisfies the callee's own constraints directly.
- **Impact:** pause, allowlist, limit, or eligibility bypass.
- **Remediation:** move enforcement into the callee/common boundary or authenticate the wrapper caller.

## T22-FLOW-004 — Onboarding and Offboarding State Are Asymmetric

- **Root cause:** enablement creates/thaws/approves multiple coupled states while disablement clears only a subset.
- **Break condition:** user, token account, extension, or registry state survives removal.
- **Impact:** retained capability, stale authority, or unusable re-onboarding.
- **Remediation:** define symmetric state transitions and reconciliation for partial/external changes.

## T22-FLOW-005 — External Balance Mutation Breaks Internal Ledger

- **Root cause:** a vault ledger assumes balances change only through protocol instructions.
- **Break condition:** permanent delegate, burn authority, fee harvest, seizure, donation, or other external action changes live balance.
- **Impact:** bad debt, reserve mismatch, unfair redemption, or settlement failure.
- **Remediation:** constrain asset authority models and reconcile live balances before sensitive operations.

## T22-FLOW-006 — Exact-Amount Assumption Differs Across Paths

- **Root cause:** only some entrypoints measure net received/spent amounts.
- **Break condition:** rebalance, liquidation, emergency, reward, or bridge paths use nominal amounts.
- **Impact:** hidden accounting drift or path-specific value extraction.
- **Remediation:** use one delta-based amount invariant across every asset movement.

## T22-FLOW-007 — Bridge or Representation Identity Is Not Bound

- **Root cause:** wrapped/bridged representation is associated by metadata or user input rather than mint, token program, chain/domain, and authority provenance.
- **Break condition:** alternate representation or recreated mint enters settlement.
- **Impact:** counterfeit redemption, wrong-asset minting, or policy escape.
- **Remediation:** bind representation identity and supply transitions to canonical provenance and domain-separated state.

## T22-FLOW-008 — Client and On-Chain Extension Policy Diverge

- **Root cause:** clients filter, resolve, or authorize an extension differently from the program.
- **Break condition:** a custom client bypasses frontend policy or an official client omits required accounts/state.
- **Impact:** fail-open acceptance, transaction denial, or inconsistent economic calculation.
- **Remediation:** enforce security on chain and share versioned deterministic builders/fixtures for client parity.
