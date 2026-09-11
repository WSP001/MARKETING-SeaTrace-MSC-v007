from __future__ import annotations

BLOCKED_PUBLIC_PATTERNS = (
    "SIMP-certified",
    "verified by NOAA",
    "verified by USDA",
    "verified by FDA",
    "live API",
    "exact coordinates",
    "price per pound",
    "SeaTrace003",
    "SeaTrace-ODOO",
    "federal verification",
    "compliance guaranteed",
    "$CHECK",
    "$BOOK",
)

PRIVATE_FIELD_NAMES = {
    "private_identity_ref",
    "exact_gps_track",
    "captain_name",
    "vessel_registration",
    "private_assertion_ref",
    "crew_notes",
    "hold_map_detail",
    "exception_notes",
    "private_invoice_ref",
    "unit_price",
    "margin",
    "customer_terms",
    "unit_cost",
    "invoice_line_id",
    "commercial_calculation",
}


def scan_text(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in BLOCKED_PUBLIC_PATTERNS if term.lower() in lowered]
