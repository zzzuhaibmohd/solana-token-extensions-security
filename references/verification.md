# Fresh Candidate Verification

Each verifier receives exactly one candidate evidence packet plus methodology. Begin from `likely false positive`, independently read all packet evidence, and apply the four gates from [judging.md](judging.md) in order.

Return exactly one verdict:

```text
VERDICT
verifier_id: V001
candidate_ids: <exact packet candidate IDs>
input_kind: FINDING|LEAD
decision: valid|valid_downgraded|valid_promoted|lead|false_positive
failed_gate: none|1|2|3|4
original_severity: Critical|High|Medium|Low|none
final_impact_tier: critical|high|medium|low|none
final_likelihood: high|medium|low|none
final_severity: Critical|High|Medium|Low|none
final_confidence: <1-100 or none>
reason: <local evidence and gate analysis>
rewrite: unchanged|follows|none
END_VERDICT
```

Contracts:

- `verifier_id` must exactly match the packet and remain in the internal audit ledger; do not expose verifier IDs in the client-facing report.
- `valid` accepts an input finding without changing its scoring.
- `valid_downgraded` accepts an input finding at a strictly lower severity and requires a narrowed rewritten finding.
- `valid_promoted` accepts an input lead only when packet evidence supplies its named missing proof and requires a rewritten finding.
- `lead` has no final scoring and requires a rewritten lead if the input was a finding.
- `false_positive` has no final scoring, identifies failed gate 1–4, and has no rewrite.
- `unchanged` is allowed only for `valid`; `follows` requires exactly one appended candidate block using the common schema; `none` forbids a block.

The rewrite must keep the same underlying mechanism, canonical identity, candidate IDs, and in-scope evidence. Recompute severity with [severity.md](severity.md). A verifier may narrow, demote, or reject a claim, but may not invent a different vulnerability.
