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

Metadata, group, and member-style mint data can live either inside the mint extension area or in a separate account. Anyone can create a metadata, group, or group-member account and point it at a legitimate mint, so the mint-pointer relationship is the authoritative trust check.

Permanent delegate is a high-risk mint authority. If present, it can transfer or burn from any token account for that mint, and transfer paths may automatically authorize it without requiring the source account owner.

Interest-bearing mints use a fixed timestamp-based formula for UI conversions. If a project expects a different interest model, or if it relies on slot-based or custom rate calculations, this extension is not a drop-in fit.

Transfer-fee mints need explicit accounting for net received amounts, fee rounding, fee configuration delay, and withheld-fee harvesting. Do not treat `calculate_fee` and `calculate_inverse_fee` as strict inverses, and do not assume `withheld_amount` is real-time without harvesting.

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

## Real Issue Patterns

These are the three audit patterns currently encoded from the issue bank:

### Transfer-Fee Accounting Drift

Look for:
- vaults or reserves that record the nominal transfer amount rather than the net received amount
- deposit, withdraw, stake, reward, or rebalance flows that assume fee-bearing transfers are 1:1
- code that ignores fee rounding, `calculate_pre_fee_amount`, or withheld-fee harvesting

Impact:
- slow insolvency
- user balance drift
- reserve accounting mismatch

Fix direction:
- book net received amounts
- use fee-aware transfer paths
- reconcile balances before and after sensitive flows

### Nominal Credit vs Spendable Balance Mismatch

Look for:
- vaults, reserves, or user-credit ledgers that record a nominal input amount instead of observed received balance
- deposit, exit, fee, or reward flows that trust the sender-side transfer amount without reconciling the receiver-side delta
- state variables that are later treated as fully spendable even though the underlying token account may have received less

Impact:
- accounting insolvency
- withdrawal DoS
- silent underpayment or over-crediting
- payout failure during later settlement or cleanup paths

Fix direction:
- measure the actual receiver-side balance delta
- store or credit the observed amount rather than the nominal input when the token behavior can differ
- cap later payouts by the real spendable balance and fail with an explicit insolvency error if needed

### Token Account Mint and Authority Binding

Look for:
- token-account inputs that are not constrained to the expected mint
- code that confuses token-account `owner`, transfer authority, and the token program itself
- CPI / transfer flows that accept arbitrary authority accounts without verifying they match the source owner or approved delegate
- protocols that silently assume ATA-only behavior even when generic token accounts are valid
- freeze / close authority that is present but not explicitly policy-checked

Impact:
- unrelated token routing
- failed or misdirected transfers
- stale delegate or authority abuse
- operational lockups from unexamined freeze or close policy

Fix direction:
- enforce mint consistency on every token account input
- validate authority binding against the source account owner or approved delegate
- require explicit protocol policy for freeze / close authority
- decide whether the protocol supports ATAs only or any valid token account, and enforce that choice consistently

### Permanent-Delegate Vault Custody Break

Look for:
- shared vaults or custody pools that accept arbitrary mints without trust-listing the delegate model
- reserve accounting that assumes no external authority can transfer or burn vault balances
- missing policy or monitoring for mints with permanent delegate enabled

Impact:
- direct vault drain
- reserve depletion
- protocol insolvency

Fix direction:
- trust-list mints and authorities
- explicitly model permanent-delegate power
- reject or isolate untrusted mints

### Transfer-Hook Integration Gap

Look for:
- hook-enabled mints passed through code paths that do not forward extra accounts
- hook-enabled mints passed through code paths that do not forward `remaining_accounts` / extra-account metas
- CPIs that omit mint-aware transfer details or rely on plain `transfer`
- hook paths that do not verify supported mints, transferring state, and token-account ownership

Impact:
- transfer failure
- missing policy enforcement
- integration-level DoS

Fix direction:
- forward the required extra accounts
- use mint-aware transfer instructions
- validate hook-supported mint sets explicitly

### Remaining-Accounts Forwarding Gap

Look for:
- manually constructed CPI instructions that hardcode `remaining_accounts_info` to `None`
- wrapper functions that never forward `remaining_accounts` into downstream CPI calls
- token-hook-aware flows that support some mints but drop the extra account payload required by hook-enabled paths

Impact:
- CPI failure when downstream programs require extra accounts
- inability to support hook-enabled or extra-account-driven token flows
- exit, collect, reward, or settlement paths becoming unusable for compatible mints

Fix direction:
- forward `remaining_accounts` whenever the downstream program may need extra account metas
- treat hook-aware CPIs as data-driven, not fixed-arity, wrappers
- test the wrapper with at least one hook-enabled mint and one no-hook mint

### Mint Extension Sizing Failure

Look for:
- mint size computed before conditional extensions are appended to the extension list
- `create_account` / mint creation paths that size the account from an empty or incomplete extension vector
- extension initialization CPIs executed after the mint was created with insufficient space

Impact:
- create-time failure
- metadata-enabled or extension-enabled flows become unavailable
- full DoS on mint creation or feature enablement paths

Fix direction:
- construct the full extension list first
- calculate mint size only after all conditional extensions are present
- size the mint for the final extension set before calling `create_account`

### Confidential Proof Validation Truncation

Look for:
- confidential mint, burn, or transfer validation code that uses `zip` or any length-limited comparison over proof commitments
- proof extraction routines that compare only the prefix of an expected commitment array
- unused proof commitments that are not explicitly required to be zero

Impact:
- malformed confidential-transfer proofs can evade full validation
- off-chain bugs in commitment assembly become harder to detect
- mint, burn, or transfer verification can accept inputs with hidden extra commitments

Fix direction:
- validate the full expected commitment set
- require all unused proof commitments to be zero
- do not rely on `zip` when extra elements must also be checked

### Multi-Leg Token-Program CPI Mismatch

Look for:
- CPI builders that reuse one token-program account across multiple CPI legs
- multi-asset instructions that accept both SPL Token and Token-2022 inputs but only thread one token program through
- duplicated `token_program` / `token_program_base` / equivalent accounts that drive separate CPI legs without a deliberate single-program policy
- any instruction that mixes token-program domains but does not pass the correct program account to each leg

Impact:
- CPI failure when different legs require different token programs
- protocol paths that work for one asset pair but break for mixed SPL Token / Token-2022 combinations
- integration DoS during redeem, withdraw, or settlement operations

Fix direction:
- pass the correct token-program account to each CPI leg explicitly
- only reuse one token-program account when the protocol truly enforces a single token-program family
- validate mixed-program paths during integration tests with at least one SPL Token and one Token-2022 asset pair

### Program-Aware ATA Derivation

Look for:
- expected associated token accounts derived with legacy SPL-only helpers in Token-2022-aware flows
- ATA validation that compares against a canonical address without threading the token program id into the derivation
- account constraints that assume associated token addresses are identical across SPL Token and Token-2022

Impact:
- valid Token-2022 ATA rejected as invalid
- finalize, claim, deposit, or settlement flows blocked by the wrong canonical account assumption
- compatibility DoS when Token-2022 assets are supported but not derived correctly

Fix direction:
- derive the expected ATA with a token-program-aware helper or explicit token program id
- pin the supported token-program family if only one is intended
- test the path separately with SPL Token and Token-2022 mints

## Transfer Fees

Look for:
- escrow or vault logic crediting the nominal amount instead of net received amount
- missing use of fee-aware transfer instructions
- code mixing `calculate_fee` and `calculate_inverse_fee` as if they are true inverses
- code assuming `calculate_pre_fee_amount` is interchangeable with fee estimates derived elsewhere
- close-account flows that ignore `withheld_amount`
- logic that assumes source and destination deltas match
- fee updates assumed to take effect immediately instead of after the epoch delay
- fee configs that leave `maximum_fee` unset or incorrectly defaulted
- code that assumes `TransferFeeConfig.withheld_amount` is synchronized with every transfer in real time

Impact:
- accounting mismatch
- undercollateralization
- stuck close flows
- silent long-tail rounding loss from 1-unit mismatches across volume
- fee bypass in edge cases involving stale accounts or reinitialized mints
- hidden 2-epoch delay where fee config changes have not yet taken effect
- inaccurate withheld-fee reporting until harvest is invoked

Fix direction:
- use fee-aware instructions where possible
- prefer `transfer_checked_with_fee` with the exact expected fee
- compare balances before and after transfer
- harvest withheld fees before close
- use `calculate_pre_fee_amount` only when the protocol really needs to invert from post-fee to pre-fee amounts
- query `getTransferFeeConfig` and `getEpochFee` when you need the effective fee schedule
- treat `HarvestWithheldTokensToMint` as the synchronization step for withheld fees

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
- protocols that do not explicitly define policy for mints with permanent delegate enabled
- systems that accept deposits before verifying the permanent delegate is trusted
- missing monitoring or alerting for mint authorities that can drain assets

Impact:
- external drain or burn of vault assets
- insolvency / bad debt / reserve mismatch
- unexpected losses from delegate-authorized transfers
- unmonitored mint authority actions

Fix direction:
- trust-list mints
- model external balance mutation as possible
- recheck balances before sensitive settlement
- define and document permanent-delegate policy explicitly
- monitor or alert on permanent-delegate activity where possible
- only accept assets from mints whose permanent delegate is trusted

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
- contracts that trust separately created metadata, group, or group-member accounts without verifying the mint's pointer
- code that fails to distinguish embedded mint-side metadata from separately created accounts

Impact:
- spoofed collection membership
- fake identity or provenance
- incorrect allowlist or gating decisions
- authoritative data confusion between embedded and external accounts

Fix direction:
- verify both directions of the mint-to-metadata and mint-to-group relationships
- treat metadata, group, and group-member extensions as identity inputs when used for auth or policy
- prefer the mint's pointer as the source of truth when external and embedded data disagree

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
- projects that assume a non-timestamp interest formula
- systems that rely on strict precision between UI conversions and actual accounting
- logic that treats network timestamp drift as impossible or irrelevant

Impact:
- user-facing confusion
- incorrect display logic
- UI amount mismatch against expected interest model
- apparent balance drift when timestamps are unstable

Fix direction:
- use raw amounts for protocol accounting
- treat `AmountToUiAmount` and `UiAmountToAmount` as UI helpers, not as authoritative settlement math
- confirm the timestamp-based formula matches the project’s intended interest model before support is added

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

