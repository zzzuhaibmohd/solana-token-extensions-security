# Solana Token-2022 Security Skill

A compact audit pack for reviewing Solana programs that touch Token-2022 mints, token accounts, vaults, escrows, staking flows, AMMs, and bridges.

Token-2022 changes the rules around:
- transfer fees
- transfer hooks
- permanent delegates
- mint close authority
- memo-required transfers
- default frozen accounts
- mint/account sizing
- metadata and group identity
- confidential balances
- wrapped SOL identity

## What’s Inside

- `SKILL.md` - main review workflow and heuristics
- `references/token-2022-patterns.md` - extension patterns and real issue classes
- `references/finding-templates.md` - report template, confidence matrix, Alice/Bob PoC framing

## Quick Start

```bash
git clone https://github.com/zzzuhaibmohd/solana-token-extensions-security.git
cd solana-token-extensions-security
```

Open these files first:
- [`SKILL.md`](./SKILL.md)
- [`references/token-2022-patterns.md`](./references/token-2022-patterns.md)
- [`references/finding-templates.md`](./references/finding-templates.md)

## How to Use

### Claude Code

Use this repo as a review playbook and ask Claude to audit the target project with a Token-2022 lens.

Example:

```text
Audit this Solana codebase using SKILL.md.
Look for Token-2022 extension bugs, incorrect accounting, unsafe CPI assumptions, and mint/reinitialize risks.
Return findings with severity, confidence score, evidence, Alice/Bob scenario, exploit path, and fix.
```

### Cursor

Keep `SKILL.md` open while reviewing the target codebase in Cursor, then search for the high-signal terms and compare behavior against `references/token-2022-patterns.md`.

### Codex

Load `SKILL.md` into context, use the issue bank while triaging, and format findings with `references/finding-templates.md`.

## Reporting Style

Every finding should include:
- Severity
- Confidence
- Confidence Score `0.0` to `1.0`
- Evidence
- Alice/Bob Scenario
- Exploit Path
- Fix

## Parallel Review

For bigger audits, split the work into parallel passes:
- transfer flows, fees, hooks, and memo constraints
- mint lifecycle, sizing, close-and-reinitialize, and authority model
- metadata, group identity, WSOL identity, program IDs, and interface selection
- vault, escrow, staking, and live balance reconciliation
- manual CPI wrappers and `remaining_accounts` forwarding

## Contribute

Open to contributors. If you find a new pattern:
1. Add it to `references/token-2022-patterns.md`
2. Add a report-ready line to `references/finding-templates.md`
3. Add a short heuristic to `SKILL.md` if it’s broadly useful

Suggestions and improvements are welcome, especially if they generalize well across different Solana protocols.

## References

Built from:
- [Token-2022 Security Best Practices, Part 1](https://blog.offside.io/p/token-2022-security-best-practices-part-1)
- [Token-2022 Security Best Practices, Part 2](https://blog.offside.io/p/token-2022-security-best-practices-part-2)
- [Neodyme: Token-2022 TL;DR](https://neodyme.io/en/blog/token-2022/#tldr)
- [0xFrankCastle Token-2022 audit thread](https://x.com/0xcastle_chain/status/2031497044775366770)
- [RareSkills Solana Tutorial (60 Days)](https://rareskills.io/solana-tutorial)
