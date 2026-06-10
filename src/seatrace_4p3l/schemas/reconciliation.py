from __future__ import annotations

from pydantic import Field, model_validator
from typing_extensions import Self

from seatrace_4p3l.schemas.base import SeaTraceModel
from seatrace_4p3l.schemas.enums import GateStatus, VarianceLabel


class ReceivingReconciliationEvent(SeaTraceModel):
    scenario_id: str
    catch_estimate_id: str
    harvest_index_id: str
    estimated_weight: float = Field(gt=0)
    received_weight: float = Field(gt=0)
    weight_uom: str
    variance_percent: float
    variance_label: VarianceLabel
    public_state_transition: GateStatus
    private_companion_control: GateStatus
    blocked_terms_scan: GateStatus
    provenance_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def atomicity_is_required(self) -> Self:
        gates = (
            self.public_state_transition,
            self.private_companion_control,
            self.blocked_terms_scan,
        )
        if any(gate != GateStatus.PASS for gate in gates):
            raise ValueError("reconciliation cannot advance unless every gate passes")
        return self


def calculate_variance_percent(estimated_weight: float, received_weight: float) -> float:
    if estimated_weight <= 0:
        raise ValueError("estimated_weight must be positive")
    return round(((received_weight - estimated_weight) / estimated_weight) * 100, 2)


def label_variance(variance_percent: float) -> VarianceLabel:
    absolute = abs(variance_percent)
    if absolute <= 5:
        return VarianceLabel.WITHIN_RANGE
    if absolute <= 12:
        return VarianceLabel.WATCH
    return VarianceLabel.EXCEPTION
