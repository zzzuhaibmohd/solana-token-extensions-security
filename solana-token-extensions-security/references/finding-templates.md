# Finding Templates

Use this file to turn review notes into concise, high-signal findings.

## Minimal Finding Template

### Title

Use an exploit-focused title.

Examples:
- Transfer-fee mint causes escrow over-crediting
- Close-and-reinitialize mint bypasses extension-dependent safety assumptions
- Permanent delegate can externally drain protocol vault
- Default-frozen token account bricks escrow initialization

### Preconditions

State:
- required mint or account extensions
- attacker capabilities
- whether arbitrary mints or accounts are accepted

### Bug

Describe the protocol assumption that fails.

### Exploit Path

1. Attacker prepares the mint, token account, or extension state.
2. Victim or protocol executes a normal flow.
3. Token-2022 behavior diverges from protocol expectations.
4. Funds are lost, policy is bypassed, or the flow is DoSed.

### Impact

Use concrete language:
- theft
- insolvency
- undercollateralization
- frozen funds
- stuck withdrawals
- bypassed compliance / fee / soulbound restrictions

### Fix

State:
- minimal fix
- stronger systemic fix

## Severity Heuristics

Higher severity:
- direct theft or drain
- global vault insolvency
- bypass of core collateral or accounting assumptions
- protocol-wide mint-acceptance bugs

Medium severity:
- user-specific loss
- stuck flows with practical exploitation
- accounting mismatch recoverable only with admin intervention

Lower severity:
- compatibility-only issues
- cosmetic identity confusion not used for auth or value decisions

## Review Writing Tips

- Name the broken assumption explicitly.
- Tie the bug to the extension behavior, not just to a code snippet.
- Describe the exploit path in operational terms.
- Prefer “attacker can” over “it might be possible.”
- Separate current-state checks from historical-trust issues.
- If the real issue is trust model, say that directly.

## Handy One-Liners

Use these when drafting findings:

- The protocol assumes the recipient receives the nominal transfer amount, which is false for fee-enabled Token-2022 mints.
- The protocol treats current mint configuration as proof of historical safety, which is invalid in the presence of mint close and reinitialization.
- The vault design assumes no external actor can mutate token balances, which is false when the mint exposes a permanent delegate or equivalent privileged authority.
- The flow assumes newly created token accounts are immediately usable, which is false for mints with default frozen account state.
- The transfer path assumes token movement is side-effect free, which is false for hook-enabled or memo-constrained Token-2022 assets.
