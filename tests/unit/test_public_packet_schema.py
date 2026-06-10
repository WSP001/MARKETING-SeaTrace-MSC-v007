from __future__ import annotations

from seatrace_4p3l.schemas.public_packets import (
    BuyerProofPacket,
    CatchEstimatePacket,
    HarvestIndexPacket,
    OriginContextPacket,
)


def test_public_packet_schemas_validate_fixture_sections(incoming_receiving_fixture, buyer_trace_fixture):
    origin = OriginContextPacket.model_validate(incoming_receiving_fixture["seaside"])
    catch = CatchEstimatePacket.model_validate(incoming_receiving_fixture["deckside"])
    harvest = HarvestIndexPacket.model_validate(incoming_receiving_fixture["dockside"])
    buyer = BuyerProofPacket.model_validate(buyer_trace_fixture["marketside"])

    assert origin.stage == "HOLD"
    assert catch.origin_context_id == origin.origin_context_id
    assert harvest.catch_estimate_id == catch.catch_estimate_id
    assert buyer.harvest_index_id == harvest.harvest_index_id


def test_scenario_ids_must_be_scn_prefixed(incoming_receiving_fixture):
    bad = dict(incoming_receiving_fixture["seaside"])
    bad["scenario_id"] = "REAL-LOT-001"

    try:
        OriginContextPacket.model_validate(bad)
    except ValueError as exc:
        assert "SCN-" in str(exc)
    else:
        raise AssertionError("non-scenario ID should fail")
