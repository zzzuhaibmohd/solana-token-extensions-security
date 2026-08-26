#!/usr/bin/env python3
"""Deterministically discover primary and peripheral Token-2022 audit scope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXCLUDED = {
    ".git", ".scratchpad", "target", "node_modules", "vendor", "dist", "build",
    "coverage", "generated", "fixtures", "examples", "migrations",
}
CLIENT_MARKERS = (
    "token-2022", "token_2022", "TOKEN_2022_PROGRAM_ID", "TokenzQdB",
    "get_associated_token_address_with_program_id", "getAssociatedTokenAddressSync",
    "createTransferChecked", "createTransferCheckedWithFee", "transferHook",
    "extraAccountMeta", "scaledUiAmount", "confidentialTransfer",
)
PERIPHERAL_NAMES = {
    "Cargo.toml", "Cargo.lock", "Anchor.toml", "package.json", "pnpm-lock.yaml",
    "yarn.lock", "package-lock.json", "bun.lockb", "tsconfig.json",
}


def excluded(path: Path, root: Path) -> bool:
    return any(part in EXCLUDED or part.startswith(".slot-zero-token-audit-") for part in path.relative_to(root).parts)


def discover(root: Path) -> dict[str, list[str]]:
    primary: list[str] = []
    peripheral: list[str] = []
    supporting: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or excluded(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        if path.name in PERIPHERAL_NAMES or path.suffix.lower() in {".json"} and "idl" in {p.lower() for p in path.parts}:
            peripheral.append(rel)
            continue
        if path.suffix == ".rs":
            if path.name.endswith(("_test.rs", "_tests.rs")) or "tests" in path.relative_to(root).parts:
                supporting.append(rel)
            else:
                primary.append(rel)
            continue
        if path.suffix.lower() in {".ts", ".tsx", ".js", ".mjs", ".cjs"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(marker.lower() in text.lower() for marker in CLIENT_MARKERS):
                if path.name.endswith((".test.ts", ".spec.ts", ".test.js", ".spec.js")) or "tests" in path.relative_to(root).parts:
                    supporting.append(rel)
                else:
                    primary.append(rel)
    return {"primary": primary, "peripheral": peripheral, "supporting": supporting}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    print(json.dumps(discover(root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
