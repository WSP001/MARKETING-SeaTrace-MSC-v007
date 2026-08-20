from __future__ import annotations

SPINE_ORDER = (
    "trip_id",
    "catch_estimate_id",
    "harvest_index_id",
    "traceability_lot_code",
    "buyer_proof_id",
)


def collect_spine(payload: dict[str, object]) -> dict[str, str]:
    spine: dict[str, str] = {}
    for key in SPINE_ORDER:
        value = payload.get(key)
        if isinstance(value, str) and value:
            spine[key] = value
    return spine


def require_full_spine(spine: dict[str, str]) -> None:
    missing = [key for key in SPINE_ORDER if key not in spine]
    if missing:
        raise ValueError(f"missing spine ids: {', '.join(missing)}")
