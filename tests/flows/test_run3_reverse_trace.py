from __future__ import annotations

import copy

import pytest

from seatrace_4p3l.flows.run3_buyer_po_reverse_trace import run_buyer_po_reverse_trace


def test_run3_builds_reverse_trace(buyer_trace_fixture):
    result = run_buyer_po_reverse_trace(buyer_trace_fixture)

    assert result["buyer_proof_id"] == "SCN-PROOF-PUB-01"
    assert result["proof_packet_status"] == "proof packet ready"
    assert tuple(result["reverse_trace_path"])[0].startswith("MarketSide")
    assert result["spine"]["trip_id"] == "TRIP-2026-SCN-0042"


def test_run3_reverse_trace_incomplete_status_raises_value_error(buyer_trace_fixture):
    bad = copy.deepcopy(buyer_trace_fixture)
    bad["marketside"]["reverse_trace_status"] = "partial"

    with pytest.raises(ValueError, match="not complete"):
        run_buyer_po_reverse_trace(bad)


def test_run3_reverse_trace_missing_spine_id_raises_error(buyer_trace_fixture):
    bad = copy.deepcopy(buyer_trace_fixture)
    del bad["marketside"]["harvest_index_id"]

    with pytest.raises(ValueError):
        run_buyer_po_reverse_trace(bad)
