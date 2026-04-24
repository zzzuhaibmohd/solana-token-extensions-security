# Finding Templates

Use this file to turn review notes into concise, high-signal findings.

When drafting a finding:
- generalize the bug class before mentioning a specific protocol
- use the protocol type as an example unless the bug is architecture-specific
- keep the wording reusable across AMMs, lending, staking, escrow, bridges, and other Solana programs whenever possible

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

### Severity

Choose one:
- High: direct theft, drain, insolvency, or protocol-wide bypass
- Medium: user-specific loss, stuck flow, or recoverable accounting mismatch
- Low: compatibility issue or limited blast radius

### Confidence

Choose one:
- High: code path is direct and confirmed by docs, tests, or a repro
- Medium: code strongly suggests the issue, but one assumption still needs verification
- Low: issue is plausible but not yet sufficiently proven

### Confidence Score

Use a numeric score from `0.0` to `1.0`.

Suggested mapping:
- `0.9` to `1.0`: direct code proof plus docs or repro
- `0.6` to `0.8`: strong code evidence, one assumption left
- `0.3` to `0.5`: plausible but missing runtime proof
- `0.0` to `0.2`: speculative or weakly supported

### Evidence

State the proof quality:
- code-only
- docs-supported
- issue-supported
- local repro
- confirmed exploit path

### Alice/Bob Scenario

Write the smallest believable exploit story:
- Alice is the attacker or adversarial user
- Bob is the protocol, keeper, vault, or victim user
- describe the minimal action sequence that turns the bug into a PoC

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

### PoC Notes

- keep the proof-of-concept path short
- use the Alice/Bob scenario to describe the steps in plain language
- include the exact extension(s) needed for the repro

## Confidence Matrix

Use this to classify certainty separately from severity:

### High Confidence
- direct code evidence
- docs or issue write-up confirm the behavior
- local repro or test demonstrates the path

### Medium Confidence
- strong code inference
- at least one assumption still needs validation
- likely exploitable, but not fully reproduced

### Low Confidence
- weak or indirect evidence
- depends on an inferred edge case
- more validation needed before filing as a finding

## Fast Parallel Review Plan

When auditing a larger codebase, split the work into parallel passes:

- Pass 1: transfer flows, fee math, hooks, memo constraints, and balance accounting
- Pass 2: mint lifecycle, extension sizing, close-and-reinitialize risk, and authority model
- Pass 3: metadata, group identity, WSOL identity, program IDs, and interface selection
- Pass 4: vault / escrow / staking semantics and live balance reconciliation

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
- The protocol trusts separately created metadata, group, or member accounts without verifying the mint's authoritative pointer, so spoofed identity data can be accepted.
- The protocol accepts a mint with `PermanentDelegate` without defining or monitoring delegate policy, so any delegate-authorized transfer can drain protocol funds.
- The protocol treats interest-bearing UI conversions as authoritative accounting, which is unsafe because the extension is timestamp-based and intended for UI representation.
- The protocol assumes transfer-fee helper calculations are exact inverses, which can create 1-unit rounding mismatches and stale-withheld accounting.
- The protocol assumes transfer-fee configuration changes are immediate, which is false because fee updates take effect only after the epoch delay.
- The protocol assumes withheld fees are real-time without harvest, which is false because `withheld_amount` is only synchronized when harvested to the mint.
- The protocol records nominal transfer amounts for a fee-bearing mint instead of net received amounts, which slowly drains vault or reserve accounting.
- The protocol records nominal transfer amounts as spendable balance, which can make later withdrawals fail when the receiver-side delta is smaller than expected.
- The protocol fails to bind token account mint, owner, and authority separately, which can route unrelated tokens or accept the wrong signer relationship.
- The protocol accepts a mint with `PermanentDelegate` without trust-listing or monitoring the delegate model, so a third party can drain protocol custody.
- The protocol accepts hook-enabled transfers without forwarding extra accounts or mint-aware transfer details, so the transfer hook can fail and DoS the flow.
- The protocol computes mint account space before appending all required extensions, so metadata-enabled mint creation fails at runtime because the account is undersized.
- The protocol reuses a single token-program account across multiple CPI legs, so mixed SPL Token / Token-2022 flows fail or route through the wrong program.
- The protocol validates confidential proof commitments with a length-limited comparison, so extra commitments can be ignored unless they are explicitly required to be zero.
- The protocol drops `remaining_accounts` from a manual CPI wrapper, so hook-enabled downstream instructions can fail even though the wrapper appears to support the token flow.
- The protocol derives expected associated token accounts with legacy SPL-only logic, so valid Token-2022 ATAs are rejected when the token program differs.
