from __future__ import annotations

from pydantic import computed_field

from seatrace_4p3l.schemas.base import AgentOutputModel
from seatrace_4p3l.schemas.enums import GateStatus


class BoundaryReviewOutput(AgentOutputModel):
    gate_status: GateStatus
    findings: tuple[str, ...]
    recommended_fix: str


class HandoffPacketOutput(AgentOutputModel):
    next_owner: str
    ready_for_handoff: bool
    blocked_reasons: tuple[str, ...]


class ReconciliationSummaryOutput(AgentOutputModel):
    scenario_id: str
    variance_label: str
    buyer_safe_summary: str


class OwnerReviewSummary(AgentOutputModel):
    summary: str
    recommendation: str

    @computed_field
    @property
    def go_granted(self) -> bool:
        return False
