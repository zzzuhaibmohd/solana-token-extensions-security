# Adversarial Judging

Start from `likely false positive`. Apply these gates in order and stop at the first failure:

1. **Attack execution:** Does a complete transaction or instruction sequence produce the claimed state transition? Account for signer privileges, CPI semantics, Token-2022 checks, atomic rollback, and extension prerequisites.
2. **Reachability:** Can the claimed handler and vulnerable branch be reached in the deployed design? Resolve local callers, constraints, feature flags, program IDs, and initialization state.
3. **Unprivileged trigger:** Can an external user, permissionless keeper, adversarial mint/account authority within the stated trust model, or attacker-selected integration input trigger it? A trusted administrator deliberately violating policy is not enough unless the protocol promises protection from that authority.
4. **Material impact:** Does the proved path cause theft, insolvency, unauthorized value movement, policy bypass, frozen funds, durable denial of a critical flow, or security-relevant accounting corruption? Compatibility inconvenience alone is not a scored finding.

A gate failure produces `false_positive`, except an incomplete but concrete path with a single named missing fact may become an unscored `lead`. Narrow overbroad claims to the strongest mechanism supported by local evidence. Never supply missing facts from another candidate or prior role conclusion.
