from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_CHAIN = (
    "trip_id",
    "catch_estimate_id",
    "harvest_index_id",
    "traceability_lot_code",
)


def _walk_dicts(value: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk_dicts(child))
    return found


def validate_no_orphans(fixture_dir: Path) -> list[str]:
    failures: list[str] = []
    seen: dict[str, set[str]] = {key: set() for key in REQUIRED_CHAIN}

    for fixture in fixture_dir.glob("*.public.json"):
        payload = json.loads(fixture.read_text())
        for item in _walk_dicts(payload):
            for key in REQUIRED_CHAIN:
                value = item.get(key)
                if isinstance(value, str):
                    seen[key].add(value)

    if not seen["trip_id"] or not seen["catch_estimate_id"]:
        failures.append("missing SeaSide/DeckSide spine anchors")
    if not seen["harvest_index_id"] or not seen["traceability_lot_code"]:
        failures.append("missing DockSide/MarketSide spine anchors")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_dir", nargs="?", default="data/fixtures")
    args = parser.parse_args()
    failures = validate_no_orphans(Path(args.fixture_dir))
    if failures:
        print("\n".join(failures))
        return 1
    print("NO_ORPHAN_EVENT_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
