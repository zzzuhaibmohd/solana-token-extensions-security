---
name: solana-token-extensions-security
description: Use when reviewing Solana or Anchor code that interacts with Token-2022 mints, token accounts, vaults, escrows, AMMs, lending markets, staking systems, or bridges. Focus on finding security bugs caused by Token-2022 mint extensions, account extensions, authority misuse, unsafe CPI assumptions, incorrect accounting, and missing validation of token state, mint provenance, transfer hooks, transfer fees, frozen defaults, delegates, close-and-reinitialize risk, and confidential-transfer edge cases.
---

# Solana Token-2022 Security Review

Use this skill when auditing Solana programs that accept, create, custody, or transfer Token-2022 assets.

Read [token-2022-patterns.md](references/token-2022-patterns.md) when you need extension-specific exploit ideas, edge cases, or review prompts.

Read [finding-templates.md](references/finding-templates.md) when writing findings, triaging severity, or converting review notes into clean report language.

Use the issue bank in [token-2022-patterns.md](references/token-2022-patterns.md) to map real audit findings to recurring Token-2022 failure modes:
- fee accounting drift on transfer-fee mints
- nominal credit vs spendable balance mismatches
- permanent-delegate vault custody breaks
- transfer-hook integration gaps and missing extra accounts
- remaining-accounts forwarding gaps in manual CPI wrappers
- mint-extension space is computed before all required mint extensions are added
- mixed token-program CPI wiring reuses one token program across multiple CPI legs
- confidential proof validation truncates after the expected prefix and ignores unused commitments

Use the confidence matrix in [finding-templates.md](references/finding-templates.md) to record how sure you are about each finding separately from severity.

When adding or writing findings, generalize the bug class whenever possible:
- describe the reusable Token-2022 failure mode first
- use protocol-specific examples only as illustrations
- only keep protocol-specific wording when the bug truly depends on that architecture

For larger audits, split the review into parallel passes when possible:
- one pass for transfer flows, accounting, fees, hooks, and memo constraints
- one pass for mint lifecycle, extension sizing, close-and-reinitialize risk, and authority model
- one pass for metadata, group, WSOL identity, program IDs, and interface-selection ambiguity
- one pass for vault / escrow / staking semantics and live balance reconciliation
- one pass for CPI wiring that spans both SPL Token and Token-2022 accounts or multiple token programs in the same instruction
- one pass for confidential-proof validation and commitment extraction bugs
- one pass for manual CPI wrappers that may need `remaining_accounts` forwarding

Assume the target may be vulnerable whenever it:
- trusts mint/account state without verifying extensions
- assumes all SPL-like tokens behave like classic SPL Token
- assumes transfers are synchronous, full-amount, transferable, unfrozen, or memo-free
- trusts mint addresses without considering close-and-reinitialize history
- treats token balances as invariant despite permanent delegates, mint authorities, or seizure-style controls
- hardcodes token-account size, rent, or closeability assumptions from classic SPL Token

Token-2022 token accounts keep the classic SPL Token account layout and append extension data. Treat every token account as potentially carrying extra rules that affect transferability, closure, ownership, or confidentiality.

Token-2022 mint accounts also append extension data. Treat every mint as potentially carrying extra rules that affect supply, fees, transfer policy, account state, identity, provenance, or group membership.

Mint extensions are fixed at creation time. Plan the full extension set up front, and respect any dependency constraints between mint extensions before initialization succeeds.

Permanent delegate on a mint is a high-risk authority. If present, it can transfer or burn from any token account for that mint, and transfer paths may authorize it automatically.

Interest-bearing mints use a fixed timestamp-based formula for UI conversions. If a project expects a different interest model, or if it relies on slot-based or custom rate calculations, this extension is not a drop-in fit.

Transfer-fee mints need explicit accounting for net received amounts, fee rounding, fee configuration delay, and withheld-fee harvesting. Do not treat `calculate_fee` and `calculate_inverse_fee` as strict inverses, and do not assume `withheld_amount` is real-time without harvesting.

Be careful with wrapped SOL. SPL Token WSOL and Token-2022 WSOL use different mint addresses, so contracts that special-case WSOL should distinguish them explicitly and avoid treating the Token-2022 WSOL as the canonical one by default.

SPL Token and Token-2022 are separate programs with different program IDs. Any code that uses token-program SDK helpers or CPIs must make the target program explicit instead of relying on library defaults.

Before auditing a contract, decide whether it is meant to support Token-2022. If Token-2022 support is intended, `anchor_spl::token_interface` is the right path; if not, prefer classic SPL token types and avoid accidental ambiguity from interface-based helpers.

## Review Goal

Find places where protocol assumptions and Token-2022 behavior diverge.

Prioritize:
1. Fund loss
2. Bypass of protocol restrictions
3. Incorrect accounting
4. Permanent DoS on vaults / escrows / user flows
5. Trust-model mismatches that admins or mint authorities can abuse

## Core Workflow

1. Identify every place the program:
   - accepts a mint
   - creates token accounts
   - transfers tokens
   - reads balances
   - closes token accounts
   - relies on owner, delegate, freeze, or mint authority assumptions
2. Determine whether the code uses classic SPL Token or Token-2022.
3. Enumerate the protocol assumptions:
   - exact amount received
   - token always transferable
   - token account immediately usable after creation
   - token account owner immutable or meaningful
   - mint config stable forever
   - mint extensions can be added or changed later without redesigning initialization
   - token-account size is fixed after creation
   - no third party can drain or burn vault funds
   - transfers only execute local logic
   - `amount == 0` is sufficient for token-account closure
   - SPL token account size / rent values still apply
   - reallocation is a rare edge case rather than a normal lifecycle step
4. Try to falsify each assumption using Token-2022 extensions.
5. Report the issue in exploit terms:
   - attacker setup
   - violating extension behavior
   - vulnerable assumption
   - user impact
   - minimal fix

## Fast Triage Questions

Ask these immediately during review:
- Can the protocol accept arbitrary mints?
- Does it rely on vault balances always matching internal accounting?
- Does it assume `transfer(amount)` means recipient received `amount`?
- Does it assume a newly created token account is usable immediately?
- Does it ever close and recreate mints, or trust mints created externally?
- Does it assume token accounts are normal ATAs with standard behavior?
- Does it call into token transfers without handling hooks, memos, fees, freezes, or CPI restrictions?
- Does it use a single vault for tokens whose mint authorities can seize, burn, or drain balances?
- Does it hardcode token account rent, account size, or closure conditions?
- Does it still call plain `transfer` instead of `transfer_checked` or `transfer_checked_with_fee`?
- Does any keeper, relayer, or backend create token accounts for users using user-influenced extension space?
- Does mint initialization assume extensions can be added later?
- Does any CPI path reuse one token-program account across multiple CPI legs in the same instruction?
- Does any manual CPI wrapper hardcode `remaining_accounts_info` to `None` or otherwise drop extra account metas?

If the answer to any is yes, inspect Token-2022 extension interactions before trusting the design.

## High-Signal Search Patterns

Search for these first:
- `transfer`
- `transfer_checked`
- `mint_to`
- `burn`
- `close_account`
- `approve`
- `set_authority`
- `freeze_account`
- `thaw_account`
- `InterfaceAccount<'info, Mint>`
- `InterfaceAccount<'info, TokenAccount>`
- `TokenInterface`
- `token::mint =`
- `associated_token`
- `spl_token_2022`
- `withheld_amount`
- `StateWithExtensions`
- `BaseStateWithExtensions`
- `closable()`
- `calculate_fee`
- `calculate_inverse_fee`
- `getMinimumBalanceForRentExemptAccountWithExtensions`
- `MintRequiredForTransfer`
- `anchor_spl::token::transfer`
- `transfer_checked_with_fee`
- `165`
- `reallocate`
- `createReallocateInstruction`
- `token_program_base`
- `token_program`
- `So11111111111111111111111111111111111111112`
- `9pan9bMn5HatX4EJdBwg9VgCa7Uz5HL8N1m5D3NdXejP`
- `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
- `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
- `anchor_spl::token_interface`
- `anchor_spl::token::Token`
- `zip`

Also search for logic that:
- compares expected and actual token balances
- assumes balance deltas equal requested transfer amounts
- creates vaults or escrows and uses them immediately
- allowlists mints without provenance checks
- derives PDAs without including `mint.key()`
- hardcodes `165` bytes or static token-account rent
- closes accounts using only `amount == 0`
- creates token accounts for users from keeper or relayer infrastructure
- initializes the mint before initializing the intended extensions
- reallocates token accounts without deciding who pays the extra rent
- initializes a mint without satisfying mint-extension dependency constraints
- stores mint-derived state as if the mint can never be closed and recreated
- calls deprecated plain `transfer` on Token-2022 paths that need mint-aware transfer details
- special-cases WSOL without distinguishing SPL Token WSOL from Token-2022 WSOL
- relies on SDK defaults that point at the SPL Token program when Token-2022 is intended
- mixes `token_interface` helpers into a contract that is not meant to support Token-2022
- reuses a single token-program account across multiple CPI legs in the same instruction
- validates confidential proof commitments with a prefix-only comparison
- drops `remaining_accounts` from a CPI wrapper that may need extra account metas

## Extension Review Checklist

Use the extension checklist in [token-2022-patterns.md](references/token-2022-patterns.md) for detailed extension-by-extension review prompts.

At minimum, inspect mint-side extensions:
- non-transferable tokens
- transfer fees
- transfer hook
- confidential transfer
- confidential transfer fee
- mint close authority
- default account state
- interest-bearing tokens
- permanent delegate
- metadata pointer
- metadata
- group pointer
- group
- group member pointer
- group member

Issue-derived review patterns:
- Transfer-fee accounting drift: confirm the protocol books the net received amount, not the nominal transfer amount, and uses fee-aware helpers wherever rounding or withheld-fee state matters.
- Nominal credit vs spendable balance mismatch: confirm the protocol measures the receiver-side delta when the token behavior can reduce the credited amount.
- Permanent-delegate custody break: confirm the protocol trust-lists the mint and its delegate model before accepting deposits into shared vaults or reserves.
- Transfer-hook integration gap: confirm hook-enabled mints are supported end to end, including `remaining_accounts` / extra-account metas, mint-aware transfer instructions, and CPI forwarding where required.
- Mint-extension sizing failure: confirm the mint-space calculation happens only after every conditional extension has been added to the extension list.
- Multi-leg token-program CPI mismatch: confirm each CPI leg receives the correct token-program account and that one account is not being reused across token-program domains.
- Confidential proof validation truncation: confirm every expected commitment is checked and that any unused commitments are explicitly zeroed or rejected.
- Remaining-accounts forwarding gap: confirm the wrapper forwards extra account metas whenever the downstream CPI may need them.

For metadata, group, and member-style mint identity:
- anyone can create separate metadata, group, or group-member accounts and point them at a legitimate mint
- only the data referenced by the mint's pointer is authoritative
- data may live inside the mint extension or in a separate account, so verify the mutual reference relationship before trusting it

If the protocol special-cases WSOL:
- verify whether it means SPL Token WSOL or Token-2022 WSOL
- consider blacklisting the Token-2022 WSOL mint if the product only intends to support the canonical SPL WSOL

If the protocol uses token SDK helpers or CPIs:
- verify the program ID is explicitly Token-2022 when Token-2022 behavior is required
- verify helper defaults are not silently pointing at SPL Token

Check mint-extension dependency ordering before initialization:
- confidential transfer fee requires transfer fee and confidential transfer
- transfer fee plus confidential transfer requires confidential transfer fee

At minimum, inspect mint-close behavior:
- `MintCloseAuthority`
- supply must be zero before close
- protocol state that depends on a mint not being re-created at the same address
- `Metadata`
- `Group`
- `GroupMember`
- `MetadataPointer`
- `GroupPointer`
- `GroupMemberPointer`
- `PermanentDelegate`
- `InterestBearingConfig`
- `AmountToUiAmount`
- `UiAmountToAmount`
- `calculate_pre_fee_amount`
- `getTransferFeeConfig`
- `getEpochFee`
- `HarvestWithheldTokensToMint`

At minimum, inspect:
- immutable owner
- CPI guard
- required memo on transfer
- non-transferable tokens
- transfer fees
- transfer hook
- confidential transfer
- confidential transfer fee
- token-account reallocation
- mint close authority
- permanent delegate
- default account state
- memo transfer
- token account closure logic
- rent and account-size calculation
- `transfer` vs `transfer_checked`
- metadata pointer / group pointer
- metadata / group / group member pointer

## Common Vulnerability Themes

### Theme: Exact-Amount Assumption

Red flag:
- protocol increments internal credit by requested transfer amount

Breaks under:
- transfer fees
- hooks that fail or alter flow
- memo-required destinations when transfer silently never lands
- `calculate_fee` and `calculate_inverse_fee` being mixed interchangeably

### Theme: Immediate-Usability Assumption

Red flag:
- protocol creates a token account and immediately deposits, transfers, or escrows without checking state

Breaks under:
- default frozen accounts
- extension-incompatible token accounts

### Theme: Stable-Mint Assumption

Red flag:
- protocol allowlists by current mint state only

Breaks under:
- close-and-reinitialize

### Theme: Mint Dependency Assumption

Red flag:
- protocol assumes mint extensions can be initialized in any order or combined arbitrarily

Breaks under:
- hidden extension dependency constraints
- missing `confidential transfer` / `transfer fee` / `confidential transfer fee` ordering

### Theme: Mint-Recreate Assumption

Red flag:
- protocol stores mint-derived state as if the mint address can never be closed and recreated

Breaks under:
- `MintCloseAuthority`
- zero-supply close and reinitialization at the same address

### Theme: Permanent Delegate Assumption

Red flag:
- protocol assumes the mint cannot move or burn user funds outside normal account-owner approvals

Breaks under:
- `PermanentDelegate`
- automatic authorization of the permanent delegate in transfer paths
- vaults that trust live balances without accounting for delegate power

### Theme: Vault-Can’t-Be-Drained Assumption

Red flag:
- protocol treats live vault balance as impossible to mutate externally

Breaks under:
- permanent delegate
- mint authority power
- seizure/compliance controls

### Theme: Plain-Transfer Assumption

Red flag:
- protocol assumes transfer is only a token movement with no side effects

Breaks under:
- transfer hook
- memo transfer
- CPI guard
- calling deprecated `transfer` on Token-2022 flows that require mint-aware transfer paths
- transfer-hook or transfer-fee accounts that return `MintRequiredForTransfer` unless the mint is supplied

### Theme: Mint-Aware Transfer Assumption

Red flag:
- protocol uses `transfer` when the token path needs the mint, decimals, or expected fee

Breaks under:
- `TransferHook`
- `TransferFee`
- `transfer_checked`
- `transfer_checked_with_fee`

### Theme: Interest Formula Assumption

Red flag:
- protocol assumes the mint’s interest formula matches its own accounting model

Breaks under:
- timestamp-based UI conversion only
- slot-based or custom interest expectations
- network timestamp drift or halted production causing different UI conversions

### Theme: Fee Accounting Assumption

Red flag:
- protocol assumes transfer fees are immediately reflected as the nominal transfer amount or that fee helpers are exact inverses

Breaks under:
- `TransferFee`
- `calculate_fee` vs `calculate_inverse_fee` rounding differences
- withheld-fee values that are not synchronized until harvested
- transfer-fee config changes that do not take effect immediately

### Theme: Metadata Identity Assumption

Red flag:
- protocol trusts metadata, group, or member data without verifying the mint-pointer relationship

Breaks under:
- spoofed metadata / group / member accounts pointing at a legitimate mint
- embedded metadata living in the mint itself versus a separate account

### Theme: WSOL Identity Assumption

Red flag:
- protocol assumes there is only one wrapped SOL mint or special-cases WSOL without checking the program family

Breaks under:
- Token-2022 WSOL mint address differs from SPL Token WSOL
- ambiguous SOL/WSOL handling in DeFi integrations

### Theme: Program-ID Assumption

Red flag:
- protocol assumes SDK helpers or CPIs will automatically target the right token program

Breaks under:
- SPL Token helper defaults pointing to the SPL Token program
- explicit Token-2022 behavior requiring `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`

### Theme: Interface-Selection Assumption

Red flag:
- protocol uses `token_interface` without having decided to support Token-2022

Breaks under:
- SPL-only contracts that accidentally become ambiguous
- helper paths that should have used `anchor_spl::token::Token`

### Theme: SPL-Compat Assumption

Red flag:
- protocol hardcodes classic SPL token-account space, rent, or closure rules

Breaks under:
- extension-sized token accounts
- transfer-fee withheld balances
- confidential-transfer pending and available balances
- CPI-guard close restrictions
- mint extensions needing upfront allocation and initialization order

### Theme: Reallocation Assumption

Red flag:
- protocol assumes token-account size is fixed forever after creation

Breaks under:
- account extensions added later
- extra-rent payer mismatches
- keeper-funded account creation

## Reporting Template

Use this structure for findings:

### Title

Short, exploit-focused bug title.

### Severity

High / Medium / Low / Info.

### Confidence

High / Medium / Low.

### Confidence Score

Use a numeric score from `0.0` to `1.0`.

### Evidence

- code path
- docs or issue reference
- local repro or test result

### Alice/Bob Scenario

- Alice: attacker or adversarial actor
- Bob: victim, protocol, or keeper
- show the smallest believable exploit or PoC path between Alice and Bob

### Preconditions

- which mint/account extensions are needed
- whether attacker controls a mint, token account, or recipient
- whether protocol accepts arbitrary Token-2022 assets

### Bug

Explain the exact protocol assumption that fails.

### Exploit Path

1. Attacker prepares mint / account / extension state.
2. Victim or protocol executes normal flow.
3. Extension behavior diverges from protocol assumption.
4. Funds are lost, accounting breaks, or the protocol is DoSed.

### Impact

State concrete effect:
- theft
- insolvency
- frozen funds
- bypassed KYC / fees / soulbound restrictions
- stuck closes

### Fix

State minimal fix and strongest fix.

Use severity and confidence separately:
- severity measures impact
- confidence measures certainty
- evidence explains why the confidence rating is justified
- confidence score should reflect how much of the exploit path is proven, not how severe the impact is
- Alice/Bob scenario should be short, concrete, and easy to convert into a PoC

## Strong Default Heuristics

Default to suspicion when:
- arbitrary user-supplied mints are accepted
- vault balances are trusted without reconciliation
- extension state is never inspected
- current mint data is treated as history
- token accounts are assumed to be standard ATAs
- token logic does not branch on Token-2022 features
- account creation or closing logic reuses classic SPL constants and assumptions

Default to lower severity when:
- the extension is cosmetic only and not used for auth or accounting
- the protocol explicitly trust-lists mints and authorities
- live balance checks and post-transfer reconciliation already exist

## Scope Notes

This skill is optimized for:
- Anchor programs
- Solana token vaults
- AMMs
- lending / margin / borrow-lend systems
- bridges
- staking systems
- escrow contracts
- NFT / collection logic using Token-2022 metadata or group features

When auditing a new extension, add it by preserving this format:
- what the extension changes
- broken protocol assumptions
- exploit shape
- impact
- minimal fix

When writing a new pattern, prefer reusable language over protocol-specific language:
- write the general bug class
- note the affected protocol type only as an example
- keep the heuristic useful across multiple Solana codebases whenever possible
