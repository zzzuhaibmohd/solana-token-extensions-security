#!/usr/bin/env python3
"""Self-test Rust and Token-2022 client scope discovery."""

from __future__ import annotations

import tempfile
from pathlib import Path

from discover_scope import discover


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="slot-zero-token-v2-test-") as raw:
        root = Path(raw)
        write(root / "programs/vault/src/lib.rs", "use spl_token_2022::extension::StateWithExtensions;")
        write(root / "clients/token.ts", "import { TOKEN_2022_PROGRAM_ID } from '@solana/spl-token';")
        write(root / "clients/unrelated.ts", "export const answer = 42;")
        write(root / "tests/token.test.ts", "const p = TOKEN_2022_PROGRAM_ID;")
        write(root / "target/generated.rs", "ignored")
        write(root / "Cargo.toml", "[workspace]\n")
        result = discover(root)
        assert result["primary"] == ["clients/token.ts", "programs/vault/src/lib.rs"], result
        assert result["supporting"] == ["tests/token.test.ts"], result
        assert result["peripheral"] == ["Cargo.toml"], result
    print("DISCOVERY TEST PASSED: Rust, Token-2022 client, supporting test, and exclusions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
