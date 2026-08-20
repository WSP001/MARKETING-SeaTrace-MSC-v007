from __future__ import annotations

from pydantic import Field

from seatrace_4p3l.schemas.base import SeaTraceModel


class FinishedProductIndexRecord(SeaTraceModel):
    scenario_id: str
    source_harvest_id: str
    traceability_lot_code: str
    sku_label: str
    case_count_band: str
    package_format: str
    qr_status: str
    source_spine: dict[str, str]
    provenance_hash: str = Field(min_length=12)


def index_finished_product(payload: dict[str, object]) -> FinishedProductIndexRecord:
    return FinishedProductIndexRecord.model_validate(payload)
