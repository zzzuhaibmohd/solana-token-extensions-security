# R3 — Hooks, Dynamic Accounts, and CPI Trust

Review the complete source bundle and [03-hooks-cpi.md](../patterns/03-hooks-cpi.md).

Trace transfer-hook execution across on-chain instructions and client resolvers. Verify mint-aware transfer construction, extra-account-metas PDA namespaces, ordered dynamic account resolution, remaining-account forwarding, semantic role binding, hook program identity, executable checks, signer/writable privilege minimization, CPI guard behavior, memo sequencing, and copied discriminators or layouts. Inspect every wrapper and alternate entrypoint that can bypass the intended hook-aware path.

Executable status alone never proves program identity. A missing extra account is a finding only when it creates material denial or fail-open behavior, not ordinary unsupported integration. Return only blocks from [shared-rules.md](../shared-rules.md) using `R3-###` IDs.
