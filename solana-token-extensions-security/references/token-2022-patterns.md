# Token-2022 Patterns

Use this file when you want extension-specific exploit ideas, broken assumptions, and fix directions during review.

Token-2022 token accounts are classic SPL accounts plus extension data. On the account side, the recurring extensions you should expect are:
- immutable owner
- CPI guard
- required memo on transfer
- non-transferable
- transfer fees
- transfer hook
- confidential transfer
- confidential transfer fee

Token-2022 mint accounts are classic SPL mints plus extension data. On the mint side, the recurring extensions you should expect are:
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

Mint extensions are fixed at creation time. If a mint needs multiple extensions, make sure you satisfy any dependency ordering before initialization.

Wrapped SOL has two common mint addresses in the ecosystem:
- SPL Token WSOL: `So11111111111111111111111111111111111111112`
- Token-2022 WSOL: `9pan9bMn5HatX4EJdBwg9VgCa7Uz5HL8N1m5D3NdXejP`

If a protocol special-cases WSOL, make sure it distinguishes these addresses explicitly. For products that only intend to support canonical SPL WSOL, blacklisting the Token-2022 WSOL mint can avoid ambiguity.

SPL Token and Token-2022 are separate programs with different program IDs:
- SPL Token: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
- Token-2022: `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`

When a helper or CPI can work with either program, do not rely on the SDK default. Make the intended program explicit.

Decide up front whether the contract supports Token-2022:
- if yes, prefer `anchor_spl::token_interface`
- if no, prefer classic SPL token types and avoid interface-based ambiguity

## Transfer Fees

Look for:
- escrow or vault logic crediting the nominal amount instead of net received amount
- missing use of fee-aware transfer instructions
- code mixing `calculate_fee` and `calculate_inverse_fee` as if they are true inverses
- close-account flows that ignore `withheld_amount`
- logic that assumes source and destination deltas match

Impact:
- accounting mismatch
- undercollateralization
- stuck close flows
- silent long-tail rounding loss from 1-unit mismatches across volume
- fee bypass in edge cases involving stale accounts or reinitialized mints

Fix direction:
- use fee-aware instructions where possible
- prefer `transfer_checked_with_fee` with the exact expected fee
- compare balances before and after transfer
- harvest withheld fees before close

## Mint Close Authority

Look for:
- protocols trusting the current mint state without mint provenance
- “reject closeable mints” as the only protection
- extension-dependent logic on arbitrary external mints

Impact:
- close-and-reinitialize can bypass later extension assumptions
- old token accounts may remain valid but incompatible with new mint rules

Fix direction:
- rely on trusted mint registries / provenance
- do not treat current extension state as proof of historical safety

## Permanent Delegate

Look for:
- shared protocol vaults holding tokens from untrusted mints
- accounting that assumes no external party can transfer or burn vault funds
- insolvency-sensitive designs with no recheck of live balances

Impact:
- external drain or burn of vault assets
- insolvency / bad debt / reserve mismatch

Fix direction:
- trust-list mints
- model external balance mutation as possible
- recheck balances before sensitive settlement

## Default Account State

Look for:
- vault or escrow initialization that assumes newly created accounts are usable
- transfer or mint flows into accounts immediately after creation without state checks

Impact:
- frozen-by-default accounts can brick flows or trap funds

Fix direction:
- inspect account state after creation
- thaw if authorized and intended
- fail explicitly on frozen accounts

## Memo Transfer

Look for:
- transfers into arbitrary user token accounts with no memo support
- CPI transfer flows that do not prepend memo

Impact:
- recipient-specific DoS for incoming transfers

Fix direction:
- support `memo -> transfer` sequencing
- detect and surface memo-required failures clearly

## CPI Guard

Look for:
- protocols trying to move user tokens during CPI using owner authority alone
- designs that do not use delegate approval flow

Impact:
- transfer failures
- broken integrations

Fix direction:
- use delegate-based flows
- verify transfer success after CPI

## Transfer Hook

Look for:
- protocols assuming token transfers are pure token-program operations
- missing extra-account handling
- hook programs that fail to verify supported mints
- PDAs shared across different mints
- hook programs that do not verify `transferring` state
- hook logic that trusts token accounts without checking they belong to the passed mint

Impact:
- arbitrary policy bypass
- unauthorized PDA access
- cross-mint state collisions
- unexpected transfer failures / DoS

Fix direction:
- verify mint support
- verify transferring flags
- verify token account mint matches the mint account
- include mint in PDA seeds

## Token Account Closure

Look for:
- close logic that only checks `amount == 0`
- hand-rolled closability checks instead of extension-aware checks
- CPI close flows that ignore CPI Guard destination restrictions
- close flows that ignore `TransferFeeAmount.withheld_amount`
- close flows that ignore confidential pending or available balances
- close flows that ignore `ConfidentialTransferFeeAmount.withheld_amount`
- close flows that ignore the CPI Guard destination-owner rule in CPI contexts

Impact:
- stuck user exits
- stuck escrows or vault cleanup
- full instruction reverts when close is part of a larger flow

Fix direction:
- use each extension's `closable()` logic instead of hand-rolling checks
- inspect withheld balances and confidential balances explicitly if implementing custom close flows
- if closing via CPI, enforce the owner-destination rule before invoking the close instruction

## Reallocation

Look for:
- account extensions that are added after initial account creation
- reallocate flows that do not treat extra rent as a protocol cost decision
- create-reallocate helper usage that ignores `payer`
- backend flows that assume account size can never change after creation

Impact:
- unexpected rent loss
- account creation or extension enablement failure
- keeper or protocol overpaying when users control the extension set

Fix direction:
- make reallocation an explicit part of the account lifecycle
- decide who pays additional rent before invoking reallocation
- use extension-aware rent and size calculations at the time of reallocation

## transfer vs transfer_checked

Look for:
- `anchor_spl::token::transfer`
- Token-2022 flows using plain `transfer` instead of `transfer_checked`
- Token-2022 flows using plain `transfer` instead of `transfer_checked_with_fee`
- missing mint account or decimals in transfer paths
- code that ignores `MintRequiredForTransfer`
- call sites that do not provide the mint when the token requires hook or fee resolution

Impact:
- transfers fail with `MintRequiredForTransfer`
- integrations break only for extension-enabled tokens
- fee-bearing or hook-bearing transfers revert even when the code looks valid in classic SPL Token

Fix direction:
- use `anchor_spl::token_interface`
- use `transfer_checked` for Token-2022
- use `transfer_checked_with_fee` when fee-bearing tokens are supported
- prefer mint-aware transfer paths whenever the mint can carry `TransferHook` or `TransferFee` extensions

## Dynamic Rent and Account Size

Look for:
- hardcoded `165` byte token-account assumptions
- hardcoded rent values for token accounts
- backend or keeper flows paying for user-created extension accounts
- runtime account creation that ignores `getMinimumBalanceForRentExemptAccountWithExtensions`

Impact:
- account creation failure
- keeper or relayer overpayment
- DoS for extension-bearing account creation

Fix direction:
- compute rent dynamically with extension-aware helpers
- do not assume classic SPL token-account size
- avoid keeper-funded account creation when users control the extension space

## Mint Initialization Order

Look for:
- mint creation flows that initialize the base mint before all required extensions
- designs that expect mint extensions to be added after initialization
- backend code that allocates mint space as if it were a classic SPL mint
- mint extension combinations that ignore dependency constraints

Impact:
- extension setup failure
- incorrect mint layout
- redesign pressure that leads teams toward unsafe close-and-reinitialize workflows
- mint initialization reverting because a required companion extension was not enabled

Fix direction:
- decide the full extension set up front
- allocate extension-aware mint space before initialization
- initialize required extensions before initializing the base mint
- enforce mint-extension dependency ordering in the mint-creation flow

## Mint Close Authority

Look for:
- protocol state that assumes a mint address can never be closed and recreated
- mint-derived caches or registry entries that are not refreshed after close/recreate
- close flows that do not confirm mint supply is zero before close

Impact:
- stale mint-derived state
- inconsistent protocol metadata
- close-and-recreate history that invalidates trust assumptions

Fix direction:
- treat mint close as a provenance event
- refresh mint-derived state from the canonical mint account
- do not trust a mint address alone to imply stable history

## Group Pointer / Metadata Pointer

Look for:
- logic that treats pointer presence as sufficient proof of identity
- missing bidirectional verification
- group or group-member flows that trust only one side of the pointer relationship

Impact:
- spoofed identity
- fake collections
- bad allowlist decisions

Fix direction:
- verify mint points to metadata/group
- verify metadata/group points back to mint

## Mint Identity and Grouping

Look for:
- code that assumes metadata or group membership is cosmetic and never needs validation
- allowlist or collection logic that trusts only one side of the reference
- group-member validation that does not also verify the canonical mint or group account

Impact:
- spoofed collection membership
- fake identity or provenance
- incorrect allowlist or gating decisions

Fix direction:
- verify both directions of the mint-to-metadata and mint-to-group relationships
- treat metadata, group, and group-member extensions as identity inputs when used for auth or policy

## WSOL Identity

Look for:
- contracts that special-case WSOL without checking whether the mint is SPL Token or Token-2022
- DeFi logic that assumes one canonical wrapped SOL mint
- blacklist or allowlist logic that omits the Token-2022 WSOL mint

Impact:
- ambiguous asset handling
- incorrect routing or pricing assumptions
- unintended support for Token-2022 WSOL in products that only intend canonical SPL WSOL

Fix direction:
- explicitly compare against the exact WSOL mint addresses you support
- blacklist the Token-2022 WSOL mint when the product only supports SPL WSOL

## Program ID Selection

Look for:
- SDK helpers that default to the SPL Token program ID
- CPIs that omit the token program account or pass the wrong one
- code that assumes a shared interface implies shared program behavior

Impact:
- Token-2022 instructions routed to SPL Token
- `MintRequiredForTransfer` or extension-related failures
- subtle mismatches between intended and actual token-program behavior

Fix direction:
- explicitly set the token program ID at every CPI boundary
- treat SDK defaults as unsafe unless the product only supports SPL Token

## Interface Selection

Look for:
- contracts that import `anchor_spl::token_interface` without intending to support Token-2022
- code that mixes SPL-only assumptions with interface-based token abstractions
- audit targets that do not declare a token-program support policy up front

Impact:
- ambiguous program behavior
- accidental extension compatibility exposure
- surprising CPI or account-type mismatches

Fix direction:
- decide support policy before implementation
- use `token_interface` only when Token-2022 support is intended
- use `anchor_spl::token::Token` for SPL-only contracts

## Immutable Owner

Look for:
- protocols assuming all token accounts can have owner reassigned
- ATA logic that breaks when owner is immutable

Impact:
- compatibility issues
- mistaken recovery or admin flows

Fix direction:
- do not assume owner reassignment is available

## Non-Transferable

Look for:
- code assuming all accepted collateral or deposits can later be transferred out
- liquidation or withdrawal flows that require transferability

Impact:
- stuck assets
- broken exits

Fix direction:
- reject unsupported non-transferable mints or design around burn/close-only behavior

## Interest Bearing Mint

Look for:
- protocol logic using UI amounts instead of raw amounts

Impact:
- user-facing confusion
- incorrect display logic

Fix direction:
- use raw amounts for protocol accounting

## Confidential Transfer / Confidential Transfer Fee

Look for:
- assumptions that public balances reflect spendable value
- logic ignoring pending confidential balances
- unsupported proof or account lifecycle in protocols that claim compatibility
- close or exit flows that assume public-balance semantics

Impact:
- broken accounting
- stuck user flows
- false assumptions around usable balance

Fix direction:
- distinguish public, confidential, and pending balances
- require explicit lifecycle support before claiming compatibility

## Cross-Cutting Patterns

### Exact-Amount Assumption

Red flag:
- protocol increments internal credit by requested transfer amount

Usually breaks under:
- transfer fees
- failed memo-required transfers
- hook-governed transfers
- fee rounding differences from mismatched fee helpers

### Immediate-Usability Assumption

Red flag:
- protocol creates a token account and immediately uses it without state checks

Usually breaks under:
- default frozen accounts
- extension-sensitive account setup

### Stable-Mint Assumption

Red flag:
- protocol allowlists by current mint state only

Usually breaks under:
- close-and-reinitialize

### Vault-Can’t-Be-Drained Assumption

Red flag:
- protocol treats live vault balance as impossible to mutate externally

Usually breaks under:
- permanent delegate
- trusted-authority seizure power

### Plain-Transfer Assumption

Red flag:
- protocol assumes transfer is only token movement with no side effects

Usually breaks under:
- transfer hook
- memo transfer
- CPI guard
- plain `transfer` used against Token-2022 extension-bearing accounts

### SPL-Compat Assumption

Red flag:
- protocol reuses classic SPL constants, rent values, or closability rules

Usually breaks under:
- extension-sized token accounts
- extension-specific close restrictions
- Token-2022 transfer requirements
