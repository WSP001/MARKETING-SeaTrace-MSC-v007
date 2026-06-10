from __future__ import annotations

from seatrace_4p3l.etl.receiving_adapter import (
    build_catch_estimate,
    build_harvest_index,
    reconcile_receiving,
)
from seatrace_4p3l.schemas.reconciliation import calculate_variance_percent, label_variance


def test_variance_calculation_and_labeling():
    variance = calculate_variance_percent(12000, 11420)

    assert variance == -4.83
    assert label_variance(variance) == "within_range"


def test_reconciliation_event_advances_only_with_all_gates(incoming_receiving_fixture):
    catch = build_catch_estimate(incoming_receiving_fixture["deckside"])
    harvest = build_harvest_index(incoming_receiving_fixture["dockside"])

    event = reconcile_receiving(catch, harvest)

    assert event.public_state_transition == "PASS"
    assert event.private_companion_control == "PASS"
    assert event.blocked_terms_scan == "PASS"
