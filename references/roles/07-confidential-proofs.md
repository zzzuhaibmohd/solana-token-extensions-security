# R7 — Confidential State and Proofs

Review the complete source bundle and [07-confidential-proofs.md](../patterns/07-confidential-proofs.md).

Trace confidential transfer, confidential fee, and confidential mint/burn initialization and every proof context. Verify full commitment cardinality, unused slots, proof freshness, supply snapshots, concurrent supply mutations, decryption/ciphertext state, withheld amounts, account readiness, and binding among ElGamal keys, auditor keys, registries, owners, mints, token accounts, and authorities. Resolve client proof construction alongside on-chain verification.

Do not infer cryptographic unsoundness from unfamiliar code. Identify the exact missing relation, stale statement, or unchecked commitment and prove its reachable consequence. Return only blocks from [shared-rules.md](../shared-rules.md) using `R7-###` IDs.
