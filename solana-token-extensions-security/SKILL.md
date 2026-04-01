---
name: solana-token-extensions-security
description: Use when reviewing Solana or Anchor code that interacts with Token-2022 mints, token accounts, vaults, escrows, AMMs, lending markets, staking systems, or bridges. Focus on finding security bugs caused by Token-2022 mint extensions, account extensions, authority misuse, unsafe CPI assumptions, incorrect accounting, and missing validation of token state, mint provenance, transfer hooks, transfer fees, frozen defaults, delegates, close-and-reinitialize risk, and confidential-transfer edge cases.
---

# Solana Token-2022 Security Review

Use this skill when auditing Solana programs that accept, create, custody, or transfer Token-2022 assets.

Read [token-2022-patterns.md](/Users/zuhaib44/Documents/New project 2/solana-token-extensions-security/references/token-2022-patterns.md) when you need extension-specific exploit ideas, edge cases, or review prompts.

Read [finding-templates.md](/Users/zuhaib44/Documents/New project 2/solana-token-extensions-security/references/finding-templates.md) when writing findings, triaging severity, or converting review notes into clean report language.

Assume the target may be vulnerable whenever it:
- trusts mint/account state without verifying extensions
- assumes all SPL-like tokens behave like classic SPL Token
- assumes transfers are synchronous, full-amount, transferable, unfrozen, or memo-free
- trusts mint addresses without considering close-and-reinitialize history
- treats token balances as invariant despite permanent delegates, mint authorities, or seizure-style controls

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
   - no third party can drain or burn vault funds
   - transfers only execute local logic
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

Also search for logic that:
- compares expected and actual token balances
- assumes balance deltas equal requested transfer amounts
- creates vaults or escrows and uses them immediately
- allowlists mints without provenance checks
- derives PDAs without including `mint.key()`

## Extension Review Checklist

Use the extension checklist in [token-2022-patterns.md](/Users/zuhaib44/Documents/New project 2/solana-token-extensions-security/references/token-2022-patterns.md) for detailed extension-by-extension review prompts.

At minimum, inspect:
- transfer fees
- mint close authority
- permanent delegate
- default account state
- memo transfer
- CPI guard
- transfer hook
- metadata pointer / group pointer
- immutable owner
- non-transferable
- confidential transfer / confidential transfer fee

## Common Vulnerability Themes

### Theme: Exact-Amount Assumption

Red flag:
- protocol increments internal credit by requested transfer amount

Breaks under:
- transfer fees
- hooks that fail or alter flow
- memo-required destinations when transfer silently never lands

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

## Reporting Template

Use this structure for findings:

### Title

Short, exploit-focused bug title.

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

## Strong Default Heuristics

Default to suspicion when:
- arbitrary user-supplied mints are accepted
- vault balances are trusted without reconciliation
- extension state is never inspected
- current mint data is treated as history
- token accounts are assumed to be standard ATAs
- token logic does not branch on Token-2022 features

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
