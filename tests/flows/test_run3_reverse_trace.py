from __future__ import annotations

from seatrace_4p3l.flows.run3_buyer_po_reverse_trace import run_buyer_po_reverse_trace


def test_run3_builds_reverse_trace(buyer_trace_fixture):
    result = run_buyer_po_reverse_trace(buyer_trace_fixture)

    assert result["buyer_proof_id"] == "SCN-PROOF-PUB-01"
    assert result["proof_packet_status"] == "proof packet ready"
    assert tuple(result["reverse_trace_path"])[0].startswith("MarketSide")
    assert result["spine"]["trip_id"] == "TRIP-2026-SCN-0042"
