from __future__ import annotations


def normalize_ticket_ref(raw_ref: str) -> str:
    cleaned = raw_ref.strip().upper().replace(" ", "-")
    if not cleaned.startswith("SCN-"):
        return f"SCN-{cleaned}"
    return cleaned


def normalize_weight(value: float, uom: str) -> tuple[float, str]:
    normalized_uom = uom.strip().lower()
    if normalized_uom not in {"lb", "kg"}:
        raise ValueError("weight unit must be lb or kg")
    return value, normalized_uom
