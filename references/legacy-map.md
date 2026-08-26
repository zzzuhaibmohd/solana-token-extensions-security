# Legacy v1 to v2 Coverage Map

This migration map proves that each unique v1 mechanism remains represented once. Multiple old headings map to one ID only where they described the same root cause, break condition, impact, and remediation.

| Legacy mechanism or heading | v2 pattern ID |
|---|---|
| Transfer-Fee Accounting Drift | T22-AMT-001 |
| Nominal Credit vs Spendable Balance Mismatch | T22-AMT-001 |
| Token Account Mint and Authority Binding | T22-ID-002 |
| Permanent-Delegate Vault Custody Break / Permanent Delegate | T22-AUTH-001 |
| Transfer-Hook Integration Gap / Remaining-Accounts Forwarding Gap | T22-HOOK-001 |
| Mint Extension Sizing Failure | T22-LIFE-001 |
| Confidential Proof Validation Truncation | T22-CONF-001 |
| Multi-Leg Token-Program CPI Mismatch | T22-ID-004 |
| Program-Aware ATA Derivation | T22-ID-003 |
| Instruction-Specific Extra-Account Metadata Mismatch | T22-HOOK-002 |
| Dynamic CPI Account Role Binding | T22-HOOK-003 |
| Hook or Gate Program Trust Binding | T22-HOOK-004 |
| Wrapper-Only Policy Enforcement | T22-HOOK-005 and T22-FLOW-003 |
| Extension-Integration Schema Drift | T22-HOOK-006 and T22-META-007 |
| Alternate Token Movement Bypasses Transfer-Hook Policy | T22-FLOW-001 |
| Eligibility State and Token-State Desynchronization | T22-AUTH-007 and T22-FLOW-004 |
| Transfer Fees | T22-AMT-001 through T22-AMT-004 |
| Mint Close Authority / Stable-Mint Assumption | T22-LIFE-006 |
| Default Account State / Immediate-Usability Assumption | T22-AUTH-002 and T22-LIFE-007 |
| Memo Transfer | T22-HOOK-007 |
| CPI Guard | T22-HOOK-008 |
| Transfer Hook | T22-HOOK-001 through T22-HOOK-006 |
| Token Account Closure | T22-LIFE-005 |
| Reallocation | T22-LIFE-004 |
| transfer vs transfer_checked / Plain-Transfer Assumption | T22-AMT-008 |
| Dynamic Rent and Account Size / SPL-Compat Assumption | T22-LIFE-003 |
| Mint Initialization Order | T22-LIFE-002 |
| Group Pointer / Metadata Pointer | T22-META-001 and T22-META-002 |
| Mint Identity and Grouping | T22-META-001 through T22-META-003 |
| WSOL Identity | T22-META-004 |
| Program ID Selection | T22-META-005 |
| Interface Selection | T22-META-006 |
| Immutable Owner | T22-AUTH-005 |
| Non-Transferable | T22-AUTH-006 |
| Interest Bearing Mint | T22-AMT-005 |
| Confidential Transfer / Confidential Transfer Fee | T22-CONF-001 through T22-CONF-007 |
| Exact-Amount Assumption | T22-FLOW-002 and T22-FLOW-006 |
| Vault-Can’t-Be-Drained Assumption | T22-FLOW-005 |

New v2 mechanisms are T22-AUTH-003 (Pausable), T22-AUTH-004 (Permissioned Burn), T22-AMT-006 and T22-AMT-007 (Scaled UI Amount), T22-CONF-003 (Confidential Mint/Burn proof freshness), T22-CONF-004 (cryptographic/registry binding), and T22-META-008 (feature-version drift).
