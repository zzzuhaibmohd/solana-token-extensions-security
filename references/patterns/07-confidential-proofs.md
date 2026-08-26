# Confidential State and Proof Patterns

## T22-CONF-001 — Prefix-Only Commitment Validation

- **Root cause:** `zip` or length-limited comparison validates only an expected prefix of proof commitments.
- **Break condition:** the proof carries extra commitments beyond the checked prefix.
- **Impact:** malformed confidential mint, burn, transfer, or fee statement is accepted.
- **Remediation:** validate exact cardinality and every commitment.

## T22-CONF-002 — Unused Commitments Are Not Forced to Zero

- **Root cause:** unused proof slots or optional ciphertext components are ignored rather than rejected.
- **Break condition:** attacker supplies hidden nonzero values in unused positions.
- **Impact:** statement ambiguity, supply/accounting inconsistency, or bypassed application-level constraints.
- **Remediation:** require every unused slot to equal the canonical zero representation.

## T22-CONF-003 — Confidential Mint/Burn Proof Becomes Stale

- **Root cause:** a proof binds to a supply snapshot but execution does not ensure freshness against concurrent public or confidential supply mutation.
- **Break condition:** another mint/burn changes supply between proof creation and consumption.
- **Impact:** incorrect supply transition, replay-like acceptance, or permanent transaction denial that can be adversarially induced.
- **Remediation:** bind proof context to current supply/state and consume it atomically with a freshness or nonce invariant.

## T22-CONF-004 — Cryptographic Key or Registry Binding Failure

- **Root cause:** ElGamal, auditor, decryptable-balance, registry, owner, mint, token-account, and authority identities are not checked as one relation.
- **Break condition:** attacker substitutes a valid key or registry entry belonging to another owner/mint/account.
- **Impact:** privacy failure, unauthorized confidential operation, or misattributed balance.
- **Remediation:** domain-separate and validate every key-to-owner-to-mint-to-account relation on chain and in proof construction.

## T22-CONF-005 — Confidential Fee State Is Not Settled

- **Root cause:** accounting or close paths omit encrypted withheld fees, harvest state, or authority requirements.
- **Break condition:** a confidential-fee account reaches withdrawal, settlement, or closure.
- **Impact:** lost fee value, inconsistent reserves, or permanently stuck account.
- **Remediation:** include confidential withheld state in balance reconciliation and terminal lifecycle handling.

## T22-CONF-006 — Confidential Account Readiness Assumed

- **Root cause:** a token account is used before required confidential configuration, approval, or decryptable state is initialized.
- **Break condition:** create-and-use or keeper flows target a not-yet-ready account.
- **Impact:** trapped deposit or durable flow denial.
- **Remediation:** enforce the complete confidential-account readiness state before movement.

## T22-CONF-007 — Proof Context Not Bound to Instruction Accounts

- **Root cause:** proof context account, authority, mint, source, destination, or amount is accepted without exact instruction-account binding.
- **Break condition:** a valid proof/context from another operation is reused or redirected.
- **Impact:** unauthorized confidential transfer/mint/burn or incorrect accounting.
- **Remediation:** validate proof type, context ownership, freshness, and every public input against the executing instruction.
