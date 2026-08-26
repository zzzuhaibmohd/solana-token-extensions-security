# R6 — Metadata, Interfaces, and Version Drift

Review the complete source bundle and [06-metadata-interfaces.md](../patterns/06-metadata-interfaces.md).

Verify metadata/group/member pointers and mutual identity, internal versus external data, update authorities, WSOL identity, classic/Token-2022 program IDs, Anchor interface selection, SDK defaults, IDL addresses, declared program IDs, and copied schemas. Compare features assumed by clients and programs with pinned SDK/CLI crates and the deployed Token-2022 program surface. Trace version drift to a concrete fail-open, fund lock, or durable critical-flow denial.

Untrusted metadata is a finding only when the protocol uses it for authorization, accounting, pricing, or another security decision. Return only blocks from [shared-rules.md](../shared-rules.md) using `R6-###` IDs.
