# R8 — Cross-Flow Parity and Coverage Sweep

Read [pattern-index.md](../pattern-index.md) and every file under `../patterns/`. Review the complete source bundle independently.

Build a lifecycle map covering initialization/configuration, deposit/mint/borrow/stake, transfer/swap/rebalance, withdraw/burn/repay/unstake/claim, settlement/liquidation/emergency, bridge/migration, and close/reinitialize. Compare equivalent value movement across transfer, burn/remint, revoke/issue, wrap/unwrap, bridge, seizure, and administrative paths. Test whether pause, fee, hook, memo, eligibility, authority, accounting, and identity invariants hold symmetrically. Search for gaps not owned by another role.

Return candidates using `R8-###` IDs, followed by exactly one record for every stable catalog ID:

```text
PATTERN_COVERAGE
pattern_id: T22-X-001
status: candidate-finding|candidate-lead|reviewed-no-candidate|not-applicable|unknown
candidate_ids: <matching R8 IDs or none>
evidence: <paths/handlers or reason>
END_PATTERN_COVERAGE
```

Every catalog ID must appear exactly once. `candidate-finding` and `candidate-lead` must reference matching emitted candidates; other states use `none`. Do not call a clean item safe or pass. Return only schema blocks from [shared-rules.md](../shared-rules.md) plus coverage records.
