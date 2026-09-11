from __future__ import annotations

import argparse
import json
from pathlib import Path

from seatrace_4p3l.gates.blocked_terms import PRIVATE_FIELD_NAMES
from seatrace_4p3l.schemas.public_packets import (
    BuyerProofPacket,
    CatchEstimatePacket,
    HarvestIndexPacket,
    OriginContextPacket,
)

SECTION_MODELS = {
    "seaside": OriginContextPacket,
    "deckside": CatchEstimatePacket,
    "dockside": HarvestIndexPacket,
    "marketside": BuyerProofPacket,
}


def validate_public_private_boundary(fixture_dir: Path) -> list[str]:
    failures: list[str] = []
    for fixture in fixture_dir.glob("*.public.json"):
        payload = json.loads(fixture.read_text())
        for section, model in SECTION_MODELS.items():
            value = payload.get(section)
            if isinstance(value, dict):
                leaked = sorted(set(value) & PRIVATE_FIELD_NAMES)
                if leaked:
                    failures.append(f"{fixture}:{section} leaked private fields {leaked}")
                try:
                    model.model_validate(value)
                except Exception as exc:
                    failures.append(f"{fixture}:{section} schema error {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_dir", nargs="?", default="data/fixtures")
    args = parser.parse_args()
    failures = validate_public_private_boundary(Path(args.fixture_dir))
    if failures:
        print("\n".join(failures))
        return 1
    print("PUBLIC_PRIVATE_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
