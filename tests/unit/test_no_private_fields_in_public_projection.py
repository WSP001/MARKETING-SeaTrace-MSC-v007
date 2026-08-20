from __future__ import annotations

from seatrace_4p3l.etl.public_projection import project_public_fields


def test_public_projection_routes_private_field_names_to_withheld():
    result = project_public_fields(
        scenario_id="SCN-LOT-2026-PUB-01",
        packet_type="dockside",
        candidate_fields={
            "traceability_lot_code": "SCN-LOT-2026-PUB-01",
            "variance_label": "within_range",
            "unit_cost": "PERMISSIONED",
            "margin": "PERMISSIONED",
        },
    )

    assert result.public_fields == {
        "traceability_lot_code": "SCN-LOT-2026-PUB-01",
        "variance_label": "within_range",
    }
    assert result.withheld_fields == ("unit_cost", "margin")
