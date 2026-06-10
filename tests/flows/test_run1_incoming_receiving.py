from __future__ import annotations

import copy

import pytest

from seatrace_4p3l.flows.run1_incoming_receiving import run_incoming_receiving


def test_run1_builds_origin_catch_harvest_chain(incoming_receiving_fixture):
    result = run_incoming_receiving(incoming_receiving_fixture)

    assert result["origin_context_id"] == "SCN-ORIGIN-PUB-01"
    assert result["catch_estimate_id"] == "SCN-CATCH-PUB-01"
    assert result["harvest_index_id"] == "SCN-HARVEST-PUB-01"
    assert result["variance_label"] == "within_range"
    assert result["locked"] is True


def test_run1_blocks_broken_linkage(incoming_receiving_fixture):
    bad = copy.deepcopy(incoming_receiving_fixture)
    bad["dockside"]["catch_estimate_id"] = "SCN-CATCH-MISSING"

    with pytest.raises(ValueError, match="DockSide packet"):
        run_incoming_receiving(bad)


def test_run1_blocks_deckside_origin_mismatch(incoming_receiving_fixture):
    bad = copy.deepcopy(incoming_receiving_fixture)
    bad["deckside"]["origin_context_id"] = "SCN-ORIGIN-MISSING"

    with pytest.raises(ValueError, match="DeckSide packet"):
        run_incoming_receiving(bad)


def test_run1_blocks_exception_variance(incoming_receiving_fixture):
    bad = copy.deepcopy(incoming_receiving_fixture)
    bad["dockside"]["received_weight"] = 9000
    bad["dockside"]["variance_percent"] = -25
    bad["dockside"]["variance_label"] = "exception"

    with pytest.raises(ValueError, match="MarketSide release blocked"):
        run_incoming_receiving(bad)
