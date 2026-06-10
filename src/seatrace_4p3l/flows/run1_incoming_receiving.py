from __future__ import annotations

import json
from pathlib import Path

from seatrace_4p3l.etl.receiving_adapter import (
    build_catch_estimate,
    build_harvest_index,
    build_origin_context,
    reconcile_receiving,
)


def run_incoming_receiving(payload: dict[str, object]) -> dict[str, object]:
    origin = build_origin_context(payload["seaside"])
    catch = build_catch_estimate(payload["deckside"])
    harvest = build_harvest_index(payload["dockside"])

    if catch.origin_context_id != origin.origin_context_id:
        raise ValueError("DeckSide packet must link to SeaSide origin_context_id")
    if harvest.catch_estimate_id != catch.catch_estimate_id:
        raise ValueError("DockSide packet must link to DeckSide catch_estimate_id")

    reconciliation = reconcile_receiving(catch, harvest)
    if reconciliation.variance_label == "exception":
        raise ValueError("MarketSide release blocked by exception variance")

    return {
        "origin_context_id": origin.origin_context_id,
        "catch_estimate_id": catch.catch_estimate_id,
        "harvest_index_id": harvest.harvest_index_id,
        "variance_label": reconciliation.variance_label,
        "locked": True,
    }


def main() -> None:
    fixture = Path("data/fixtures/incoming_receiving.public.json")
    payload = json.loads(fixture.read_text())
    print(json.dumps(run_incoming_receiving(payload), indent=2, default=str))


if __name__ == "__main__":
    main()
