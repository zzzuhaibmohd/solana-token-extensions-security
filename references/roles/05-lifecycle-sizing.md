# R5 — Lifecycle, Sizing, and Provenance

Review the complete source bundle and [05-lifecycle-sizing.md](../patterns/05-lifecycle-sizing.md).

Trace mint and token-account initialization order, complete extension selection, dependency constraints, account length, rent, reallocation payer and authority, immediate usability, closure conditions, withheld/confidential state, close authority, and close-and-reinitialize provenance. Check keepers and clients that calculate extension space or create accounts from user-influenced extension sets.

Separate one-time transaction failure from durable fund lock or security-relevant denial. Prove that lifecycle assumptions are reachable in supported flows. Return only blocks from [shared-rules.md](../shared-rules.md) using `R5-###` IDs.
