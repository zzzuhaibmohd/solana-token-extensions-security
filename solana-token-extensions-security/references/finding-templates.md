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
- The protocol mixes Token-2022 fee helper semantics and assumes `calculate_fee` and `calculate_inverse_fee` are interchangeable, which can introduce persistent rounding loss.
- The protocol treats current mint configuration as proof of historical safety, which is invalid in the presence of mint close and reinitialization.
- The vault design assumes no external actor can mutate token balances, which is false when the mint exposes a permanent delegate or equivalent privileged authority.
- The flow assumes newly created token accounts are immediately usable, which is false for mints with default frozen account state.
- The transfer path assumes token movement is side-effect free, which is false for hook-enabled or memo-constrained Token-2022 assets.
- The protocol assumes classic SPL token-account size, rent, or closeability rules still apply, which is false for extension-bearing Token-2022 accounts.
- The protocol uses plain `transfer` in a Token-2022 path that requires mint-aware transfer instructions, causing extension-specific transfer failure.
- The protocol uses plain `transfer` where Token-2022 requires mint-aware details, so hook or fee-bearing mints can throw `MintRequiredForTransfer`.
- The protocol assumes Token-2022 closeability is equivalent to `amount == 0`, which is false once transfer-fee, confidential-transfer, or CPI-guard extensions are active.
- The protocol assumes token-account rent and size are static, which is false for extension-bearing Token-2022 accounts and can create correctness or keeper-loss bugs.
- The mint initialization flow assumes extensions can be added later, which is false for Token-2022 mint extensions and often leads to unsafe redesign patterns.
- The protocol ignores the CPI Guard destination-owner rule on close, which can make a larger CPI flow revert even when the account amount is zero.
- The protocol treats token-account size as fixed after creation, which is false once reallocation-capable account extensions are introduced.
- The mint initialization flow ignores extension dependency constraints, which can make valid-looking mint setups fail at creation time.
- The protocol stores mint-derived state as if the mint can never be closed and recreated, which is false once `MintCloseAuthority` exists.
- The protocol treats wrapped SOL as a single canonical mint, which is false because SPL Token WSOL and Token-2022 WSOL use different mint addresses.
- The protocol relies on token SDK defaults for program ID selection, which can silently route Token-2022 logic to the SPL Token program.
- The protocol uses `token_interface` without explicitly intending to support Token-2022, which can create ambiguous behavior in an SPL-only contract.
