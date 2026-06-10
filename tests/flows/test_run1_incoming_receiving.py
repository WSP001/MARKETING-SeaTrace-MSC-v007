from __future__ import annotations

from seatrace_4p3l.flows.run1_incoming_receiving import run_incoming_receiving


def test_run1_builds_origin_catch_harvest_chain(incoming_receiving_fixture):
    result = run_incoming_receiving(incoming_receiving_fixture)

    assert result["origin_context_id"] == "SCN-ORIGIN-PUB-01"
    assert result["catch_estimate_id"] == "SCN-CATCH-PUB-01"
    assert result["harvest_index_id"] == "SCN-HARVEST-PUB-01"
    assert result["variance_label"] == "within_range"
    assert result["locked"] is True


def test_run1_blocks_broken_linkage(incoming_receiving_fixture):
    bad = dict(incoming_receiving_fixture)
    bad["dockside"] = dict(incoming_receiving_fixture["dockside"])
    bad["dockside"]["catch_estimate_id"] = "SCN-CATCH-MISSING"

    try:
        run_incoming_receiving(bad)
    except ValueError as exc:
        assert "DockSide packet" in str(exc)
    else:
        raise AssertionError("broken spine should fail")
