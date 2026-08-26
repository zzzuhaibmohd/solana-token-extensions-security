# Authority and Control Patterns

## T22-AUTH-001 — Permanent Delegate Breaks Custody

- **Root cause:** vault accounting assumes no external authority can transfer or burn deposited assets.
- **Break condition:** an accepted mint has an untrusted permanent delegate.
- **Impact:** vault depletion, insolvency, or unrecoverable reserve mismatch.
- **Remediation:** reject or isolate such mints, trust-list the delegate model, and reconcile live balances.

## T22-AUTH-002 — Default-Frozen Account Used Before Thaw

- **Root cause:** newly created token accounts are assumed immediately usable.
- **Break condition:** the mint's default account state is frozen.
- **Impact:** trapped deposits, unusable vaults, or durable lifecycle denial.
- **Remediation:** inspect state after creation and explicitly thaw only under the intended authority and policy.

## T22-AUTH-003 — Pausable State Missing on Alternate Paths

- **Root cause:** pause checks cover ordinary transfer but not every equivalent mint/account mutation or client entrypoint.
- **Break condition:** a public alternate path moves or destroys value while the mint/account is paused.
- **Impact:** emergency-control bypass or inconsistent custody state.
- **Remediation:** enumerate pause semantics and enforce them at every unavoidable economic transition.

## T22-AUTH-004 — Permissioned Burn Additional Authority Omitted

- **Root cause:** burn construction, validation, or authorization models only the owner/delegate and omits the extension's additional burn authority.
- **Break condition:** a permissioned-burn mint enters a burn, redeem, bridge, liquidation, or close path.
- **Impact:** unauthorized burn assumption, permanently blocked exit, or broken supply/accounting invariant.
- **Remediation:** detect the extension and bind the exact additional authority and signer requirements on chain and in clients.

## T22-AUTH-005 — Immutable Owner Assumption Mismatch

- **Root cause:** protocol recovery or authority rotation assumes token-account owner can change, or security assumes it cannot without verifying the extension.
- **Break condition:** account behavior differs from the assumed owner mutability.
- **Impact:** stuck recovery/rotation or unauthorized ownership transition.
- **Remediation:** inspect immutable-owner state and make owner-mutability policy explicit at onboarding.

## T22-AUTH-006 — Non-Transferable Asset Accepted into Transfer Lifecycle

- **Root cause:** protocol accepts a mint whose tokens cannot follow required deposit, withdrawal, liquidation, or bridge transfers.
- **Break condition:** a non-transferable asset reaches a flow that requires ordinary transfer semantics.
- **Impact:** trapped assets, bad debt, or permanent critical-flow denial.
- **Remediation:** reject incompatible mints or design a complete non-transferable lifecycle.

## T22-AUTH-007 — Eligibility and Frozen State Desynchronize

- **Root cause:** eligibility metadata and token-account freeze/thaw state are updated asymmetrically.
- **Break condition:** onboarding/offboarding partially updates one half or newly created accounts evade reconciliation.
- **Impact:** removed users retain transfer capability or eligible users remain locked.
- **Remediation:** make eligibility and token state one atomic invariant with reconciliation for later accounts.

## T22-AUTH-008 — Mutable Mint Authority Outside Asset Trust Policy

- **Root cause:** mint, freeze, close, fee, hook, metadata, or confidential authorities are accepted without an explicit trust decision.
- **Break condition:** an external authority changes supply, transferability, fees, identity, or access after onboarding.
- **Impact:** loss, insolvency, policy bypass, or durable fund lock.
- **Remediation:** bind accepted assets to an authority/provenance policy and revalidate mutable state where required.
