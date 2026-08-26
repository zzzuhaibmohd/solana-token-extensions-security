# R4 — Authorities and Controls

Review the complete source bundle and [04-authorities-controls.md](../patterns/04-authorities-controls.md).

Model mint, freeze, close, permanent-delegate, transfer-fee, confidential, pause, and permissioned-burn authorities. Trace custody assumptions, approvals, revocations, seizure/burn capability, default-frozen onboarding, pause parity across mint/account and alternate paths, Permissioned Burn's additional authority, immutable-owner behavior, and eligibility/freeze state coupling. Identify which authorities are trusted explicitly and which can be attacker-controlled through accepted assets.

Do not convert a clearly documented trusted-admin power into a vulnerability. Prove a violated trust boundary or protocol promise. Return only blocks from [shared-rules.md](../shared-rules.md) using `R4-###` IDs.
