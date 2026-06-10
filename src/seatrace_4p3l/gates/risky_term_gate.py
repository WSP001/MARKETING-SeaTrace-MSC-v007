from __future__ import annotations

import argparse
from pathlib import Path

from seatrace_4p3l.gates.blocked_terms import scan_text


SCAN_SUFFIXES = {".py", ".json"}


def _should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_SUFFIXES:
        return False
    if "gates" in path.parts or "__pycache__" in path.parts:
        return False
    if path.name == "private_records.py":
        return False
    return True


def scan_paths(paths: tuple[Path, ...]) -> list[str]:
    failures: list[str] = []
    for root in paths:
        for path in root.rglob("*"):
            if not path.is_file() or not _should_scan(path):
                continue
            hits = scan_text(path.read_text(errors="ignore"))
            if hits:
                failures.append(f"{path}: {', '.join(hits)}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=["src/seatrace_4p3l", "data/fixtures"])
    args = parser.parse_args()
    failures = scan_paths(tuple(Path(item) for item in args.paths))
    if failures:
        print("\n".join(failures))
        return 1
    print("RISKY_TERM_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
