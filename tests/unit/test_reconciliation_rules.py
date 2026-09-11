from __future__ import annotations

import pytest

from seatrace_4p3l.etl.receiving_adapter import (
    build_catch_estimate,
    build_harvest_index,
    reconcile_receiving,
)
from seatrace_4p3l.schemas.reconciliation import (
    ReceivingReconciliationEvent,
    calculate_variance_percent,
    label_variance,
)


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


def test_label_variance_boundaries():
    assert label_variance(5.0) == "within_range"
    assert label_variance(12.0) == "watch"
    assert label_variance(12.01) == "exception"


def test_calculate_variance_percent_rejects_non_positive_estimated_weight():
    with pytest.raises(ValueError):
        calculate_variance_percent(0, 100)

    with pytest.raises(ValueError):
        calculate_variance_percent(-1, 100)


def test_reconciliation_event_requires_all_gates():
    with pytest.raises(ValueError, match="every gate passes"):
        ReceivingReconciliationEvent(
            scenario_id="SCN-LOT-2026-PUB-01",
            catch_estimate_id="SCN-CATCH-PUB-01",
            harvest_index_id="SCN-HARVEST-PUB-01",
            estimated_weight=12000,
            received_weight=11420,
            weight_uom="lb",
            variance_percent=-4.83,
            variance_label="within_range",
            public_state_transition="PASS",
            private_companion_control="FAIL",
            blocked_terms_scan="PASS",
            provenance_hash="SCN-RECON-HASH-FAIL",
        )
