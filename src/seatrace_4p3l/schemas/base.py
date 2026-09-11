from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing_extensions import Self

from seatrace_4p3l.gates.blocked_terms import scan_text


class SeaTraceModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    @field_validator("scenario_id", check_fields=False)
    @classmethod
    def scenario_ids_are_public_safe(cls, value: str) -> str:
        if not value.startswith("SCN-"):
            raise ValueError("scenario_id must use SCN- prefix")
        return value

    @model_validator(mode="after")
    def public_values_do_not_overclaim(self) -> Self:
        payload = self.model_dump_json()
        hits = scan_text(payload)
        if hits:
            raise ValueError(f"public-forbidden phrase found: {', '.join(hits)}")
        return self


class AgentOutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
