from __future__ import annotations

from pydantic import Field

from seatrace_4p3l.gates.blocked_terms import PRIVATE_FIELD_NAMES
from seatrace_4p3l.schemas.base import SeaTraceModel


class PublicProjectionResult(SeaTraceModel):
    scenario_id: str
    packet_type: str
    public_fields: dict[str, str | int | float | bool | None]
    withheld_fields: tuple[str, ...]
    provenance_hash: str = Field(min_length=12)


def project_public_fields(
    scenario_id: str,
    packet_type: str,
    candidate_fields: dict[str, str | int | float | bool | None],
) -> PublicProjectionResult:
    public_fields: dict[str, str | int | float | bool | None] = {}
    withheld: list[str] = []

    for key, value in candidate_fields.items():
        if key in PRIVATE_FIELD_NAMES:
            withheld.append(key)
        else:
            public_fields[key] = value

    return PublicProjectionResult(
        scenario_id=scenario_id,
        packet_type=packet_type,
        public_fields=public_fields,
        withheld_fields=tuple(withheld),
        provenance_hash=f"SCN-PROJECTION-{packet_type}-001",
    )
