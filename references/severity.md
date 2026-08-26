# Severity and Confidence

## Impact by likelihood matrix

| Impact \\ Likelihood | High | Medium | Low |
|---|---|---|---|
| Critical | Critical | High | Medium |
| High | High | High | Medium |
| Medium | Medium | Medium | Low |
| Low | Low | Low | Low |

Impact tiers:

- **Critical:** systemic or effectively unlimited loss, protocol-wide insolvency, or control compromise.
- **High:** direct theft, reserve depletion, major policy bypass, or permanent loss affecting valuable assets.
- **Medium:** bounded loss, meaningful accounting corruption, or durable denial of an important asset flow.
- **Low:** limited security impact requiring narrow conditions, with no plausible major loss.

Likelihood reflects attacker access, prerequisites, reproducibility, and expected exposure—not impact.

Confidence is an integer from 1–100 and measures proof completeness. Use 90–100 for locally demonstrated paths, 80–89 for fully traced paths with small environmental assumptions, and below 80 only when material uncertainty remains. Findings below 80 must state `MANUAL CONFIRMATION REQUIRED`, omit prescriptive patch diffs, and limit remediation to behavioral guidance. Leads have no severity or confidence.
