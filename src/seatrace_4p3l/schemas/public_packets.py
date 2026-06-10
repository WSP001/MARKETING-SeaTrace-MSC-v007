from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import Field, HttpUrl, model_validator
from typing_extensions import Self

from seatrace_4p3l.schemas.base import SeaTraceModel
from seatrace_4p3l.schemas.enums import (
    GateStatus,
    MutableStatus,
    OriginConfidenceLabel,
    Pillar,
    PoBalanceState,
    ProofStatus,
    ReverseTraceStatus,
    Stage,
    VarianceLabel,
)


class OriginContextPacket(SeaTraceModel):
    scenario_id: str
    origin_context_id: str
    trip_id: str
    trip_window_start: datetime
    trip_window_end: datetime
    general_region: str
    vessel_class: str
    gear_category: str
    signal_source_type: str
    permit_context_ref: str | None = None
    origin_confidence_label: OriginConfidenceLabel
    source_document_ref: str
    pillar: Literal[Pillar.SEASIDE] = Pillar.SEASIDE
    stage: Literal[Stage.HOLD] = Stage.HOLD
    public_state_transition: GateStatus = GateStatus.PASS
    private_companion_control: GateStatus = GateStatus.PASS
    blocked_terms_scan: GateStatus = GateStatus.PASS
    provenance_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def window_is_ordered(self) -> Self:
        if self.trip_window_end < self.trip_window_start:
            raise ValueError("trip_window_end must be after trip_window_start")
        return self


class CatchEstimatePacket(SeaTraceModel):
    scenario_id: str
    catch_estimate_id: str
    origin_context_id: str
    trip_id: str
    species_common_name: str
    species_code: str
    estimated_weight: float = Field(gt=0)
    estimated_weight_uom: Literal["lb", "kg"]
    estimated_count: int | None = Field(default=None, ge=0)
    estimate_method: str
    recorded_at: datetime
    recorded_by_role: str
    mutable_status: MutableStatus
    assertion_hash: str = Field(min_length=12)
    pillar: Literal[Pillar.DECKSIDE] = Pillar.DECKSIDE
    stage: Literal[Stage.RECORD] = Stage.RECORD
    public_state_transition: GateStatus = GateStatus.PASS
    private_companion_control: GateStatus = GateStatus.PASS
    blocked_terms_scan: GateStatus = GateStatus.PASS
    provenance_hash: str = Field(min_length=12)


class HarvestIndexPacket(SeaTraceModel):
    scenario_id: str
    harvest_index_id: str
    catch_estimate_id: str
    trip_id: str
    traceability_lot_code: str
    first_receiver_ref: str
    landing_date: date
    received_weight: float = Field(gt=0)
    received_weight_uom: Literal["lb", "kg"]
    species_or_market_name: str
    product_description: str
    harvest_date_range: str
    harvest_location_general: str
    scale_ticket_ref: str | None = None
    grade_out_label: str
    variance_percent: float
    variance_label: VarianceLabel
    reference_document_type: str
    reference_document_number: str | None = None
    pillar: Literal[Pillar.DOCKSIDE] = Pillar.DOCKSIDE
    stage: Literal[Stage.STORE] = Stage.STORE
    public_state_transition: GateStatus = GateStatus.PASS
    private_companion_control: GateStatus = GateStatus.PASS
    blocked_terms_scan: GateStatus = GateStatus.PASS
    provenance_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def harvest_links_to_catch(self) -> Self:
        if not self.catch_estimate_id:
            raise ValueError("harvest packet requires catch_estimate_id")
        return self


class BuyerProofPacket(SeaTraceModel):
    scenario_id: str
    buyer_proof_id: str
    harvest_index_id: str
    trip_id: str
    catch_estimate_id: str
    traceability_lot_code: str
    product_description: str
    quantity: float = Field(gt=0)
    quantity_uom: str
    ship_date: date
    ship_from_location_general: str
    ship_to_location_general: str
    po_balance_state: PoBalanceState
    qr_trace_url: HttpUrl | str
    reverse_trace_status: ReverseTraceStatus
    proof_packet_status: ProofStatus
    chain_continuity_summary: str
    reverse_trace_path: tuple[str, str, str, str]
    source_citations: tuple[str, ...]
    cta_label: Literal["request RFP packet", "request pilot packet"]
    claim_summary: str
    pillar: Literal[Pillar.MARKETSIDE] = Pillar.MARKETSIDE
    stage: Literal[Stage.EXCHANGE] = Stage.EXCHANGE
    public_state_transition: GateStatus = GateStatus.PASS
    private_companion_control: GateStatus = GateStatus.PASS
    blocked_terms_scan: GateStatus = GateStatus.PASS
    provenance_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def reverse_trace_has_four_pillars(self) -> Self:
        expected = ("MarketSide", "DockSide", "DeckSide", "SeaSide")
        found = tuple(step.split()[0] for step in self.reverse_trace_path)
        if found != expected:
            raise ValueError("reverse_trace_path must run MarketSide -> DockSide -> DeckSide -> SeaSide")
        return self
