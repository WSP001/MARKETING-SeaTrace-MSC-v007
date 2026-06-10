from __future__ import annotations

from seatrace_4p3l.schemas.public_packets import (
    CatchEstimatePacket,
    HarvestIndexPacket,
    OriginContextPacket,
)
from seatrace_4p3l.schemas.reconciliation import (
    ReceivingReconciliationEvent,
    calculate_variance_percent,
    label_variance,
)
from seatrace_4p3l.schemas.enums import GateStatus


def build_origin_context(payload: dict[str, object]) -> OriginContextPacket:
    return OriginContextPacket.model_validate(payload)


def build_catch_estimate(payload: dict[str, object]) -> CatchEstimatePacket:
    return CatchEstimatePacket.model_validate(payload)


def build_harvest_index(payload: dict[str, object]) -> HarvestIndexPacket:
    return HarvestIndexPacket.model_validate(payload)


def reconcile_receiving(
    catch_packet: CatchEstimatePacket,
    harvest_packet: HarvestIndexPacket,
) -> ReceivingReconciliationEvent:
    variance = calculate_variance_percent(
        estimated_weight=catch_packet.estimated_weight,
        received_weight=harvest_packet.received_weight,
    )
    return ReceivingReconciliationEvent(
        scenario_id=catch_packet.scenario_id,
        catch_estimate_id=catch_packet.catch_estimate_id,
        harvest_index_id=harvest_packet.harvest_index_id,
        estimated_weight=catch_packet.estimated_weight,
        received_weight=harvest_packet.received_weight,
        weight_uom=catch_packet.estimated_weight_uom,
        variance_percent=variance,
        variance_label=label_variance(variance),
        public_state_transition=GateStatus.PASS,
        private_companion_control=GateStatus.PASS,
        blocked_terms_scan=GateStatus.PASS,
        provenance_hash="SCN-RECON-HASH-001",
    )
