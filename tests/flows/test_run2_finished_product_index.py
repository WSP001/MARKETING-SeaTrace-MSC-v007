from __future__ import annotations

from seatrace_4p3l.flows.run2_finished_product_index import run_finished_product_index


def test_run2_indexes_finished_product(finished_product_fixture):
    result = run_finished_product_index(finished_product_fixture)

    assert result["source_harvest_id"] == "SCN-HARVEST-PUB-01"
    assert result["traceability_lot_code"] == "SCN-LOT-2026-PUB-01"
    assert result["qr_status"] == "public proof bundle ready"
