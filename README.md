# Solana Token-2022 Security Skill

This repository packages a living security review skill for auditing Solana programs that interact with Token-2022 mints, token accounts, vaults, escrows, staking flows, AMMs, bridges, and related custody logic.

The goal is simple: help you find bugs caused by incorrect assumptions about Token-2022 extensions.

Token-2022 is not just "SPL Token with extras." It changes the trust model around:
- transfer fees
- transfer hooks
- permanent delegates
- mint close authority
- memo requirements
- default frozen accounts
- mint and account reallocation
- metadata and group identity
- confidential balances
- wrapped SOL identity

This repo turns those ideas into a portable review package you can reuse across Codex, Claude Code, and Cursor.

## What’s Included

- `SKILL.md`: the main audit skill and review workflow
- `references/token-2022-patterns.md`: extension-by-extension patterns, exploit ideas, and review prompts
- `references/finding-templates.md`: report templates, severity guidance, confidence matrix, and finding one-liners

## How To Use

You can use this repository as:
- a standalone audit playbook
- a reusable prompt pack for Claude Code
- a local reference bundle for Cursor
- a Codex skill package for Token-2022 reviews

## Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/zzzuhaibmohd/solana-token-extensions-security.git
cd solana-token-extensions-security
```

### 2. Open the skill files

Review these first:
- [`SKILL.md`](./SKILL.md)
- [`references/token-2022-patterns.md`](./references/token-2022-patterns.md)
- [`references/finding-templates.md`](./references/finding-templates.md)

### 3. Keep the package together

If you move the repository, keep the root structure intact:

```text
solana-token-extensions-security/
├── README.md
├── SKILL.md
└── references/
    ├── finding-templates.md
    └── token-2022-patterns.md
```

That layout is intentional so the skill remains portable and easy to reference.

## Using With Claude Code

Claude Code works best when you treat the skill as a review playbook and feed it the repo or files you want audited.

### Recommended workflow

1. Open the target Solana repository in Claude Code.
2. Add this repo or copy `SKILL.md` and the `references/` files into your working context.
3. Ask Claude Code to audit the code with a Token-2022 lens.
4. Tell it to use the issue bank and confidence matrix when reporting findings.

### Example prompt

```text
Audit this Solana codebase for Token-2022 issues using the review workflow in SKILL.md.
Focus on transfer fees, permanent delegates, transfer hooks, mint close authority, metadata/group spoofing, and mint sizing bugs.
For each finding, give severity, confidence, evidence, exploit path, and fix.
```

### Best practice

- Point Claude Code at `SKILL.md` first.
- Use `references/token-2022-patterns.md` when you want deeper extension-specific checks.
- Use `references/finding-templates.md` when converting notes into final report language.

## Using With Cursor

Cursor works well when you want the skill as a local knowledge base while you inspect code.

### Recommended workflow

1. Open the target project in Cursor.
2. Open this repository in a second tab or keep the skill files nearby.
3. Reference `SKILL.md` while reviewing the codebase.
4. Ask Cursor to compare the target code against the Token-2022 patterns in this repo.

### Example prompt

```text
Use the Token-2022 security playbook in SKILL.md to audit this codebase.
Check for transfer-fee accounting drift, permanent delegate custody risk, transfer-hook integration gaps, mint sizing failures, and close/reinitialize bugs.
Return findings with severity, confidence, evidence, and a recommended fix.
```

### Best practice

- Keep `SKILL.md` open as a live reference.
- Use the `references/` files as lookup material for extension-specific behavior.
- Ask Cursor to search for the high-signal terms listed in the skill before reviewing logic manually.

## Using With Codex

Codex can use this repository as a reusable review skill bundle.

### Recommended workflow

1. Open the target codebase.
2. Load `SKILL.md` into context.
3. Use the issue bank and finding templates while auditing.
4. Report bugs with the severity/confidence structure in `references/finding-templates.md`.

### Example prompt

```text
Use the Token-2022 security skill in SKILL.md to audit this project.
Look for extension-driven bugs, unsafe transfer assumptions, mint recreation issues, and account sizing mistakes.
Structure each finding with severity, confidence, evidence, exploit path, and fix.
```

## What To Look For

The skill is designed to catch bugs caused by wrong assumptions, especially when code:
- treats Token-2022 like classic SPL Token
- assumes transfer amounts are always exact
- assumes token accounts are immediately usable
- assumes mint state is permanent
- ignores transfer hooks, memo requirements, or fees
- trusts mint-derived metadata without verifying pointers
- hardcodes rent, account size, or closeability rules
- accepts arbitrary mints without a trust model

## Confidence And Reporting

The repo includes a built-in reporting flow:
- `Severity` tells you how bad the issue is
- `Confidence` tells you how sure you are
- `Confidence Score` gives you a numeric certainty from `0.0` to `1.0`
- `Evidence` tells you what supports the finding
- `Alice/Bob Scenario` turns the bug into a short PoC story you can test quickly

This makes it easier to triage findings consistently across real audits.

## Faster Review Workflow

For larger codebases, split the work into parallel passes when your tooling supports it:

- transfer flows, accounting, fees, hooks, and memo constraints
- mint lifecycle, extension sizing, close-and-reinitialize risk, and authority model
- metadata, group identity, WSOL identity, program IDs, and interface selection
- vault, escrow, staking, and live balance reconciliation

That approach keeps reviews faster and helps you compare findings across independent paths.

## Reference Material Used To Build The Skill

The skill was built from real Token-2022 audit notes and public references, including:

1. [Token-2022 Security Best Practices, Part 1](https://blog.offside.io/p/token-2022-security-best-practices-part-1)
2. [Token-2022 Security Best Practices, Part 2](https://blog.offside.io/p/token-2022-security-best-practices-part-2)
3. [Neodyme: Token-2022 TL;DR](https://neodyme.io/en/blog/token-2022/#tldr)
4. [0xFrankCastle thread on Token-2022 audit patterns](https://x.com/0xcastle_chain/status/2031497044775366770)

## Contributing New Findings

As you discover new issues, add them in three places:

1. Update `references/token-2022-patterns.md` with the new pattern
2. Add a report-ready one-liner to `references/finding-templates.md`
3. Add a short review heuristic to `SKILL.md` if the pattern is important enough to remember during triage

When you add a new finding, keep it general first:

- describe the reusable Token-2022 bug class
- use protocol-specific examples only as illustrations
- avoid wording that only fits one protocol unless the bug truly depends on that architecture

That keeps the package small, readable, and easy to extend over time.

## Notes

- This repo is intentionally lightweight and markdown-first.
- The skill files are meant to be copied, referenced, or embedded into other review workflows.
- The repository root is the canonical location for the skill package.
