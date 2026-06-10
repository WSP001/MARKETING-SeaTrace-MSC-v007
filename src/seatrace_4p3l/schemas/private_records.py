from __future__ import annotations

from pydantic import Field

from seatrace_4p3l.schemas.base import SeaTraceModel
from seatrace_4p3l.schemas.enums import GateStatus


class IdentityAccessControlRecord(SeaTraceModel):
    scenario_id: str
    identity_access_key: str
    private_identity_ref: str
    exact_gps_track_ref: str
    captain_ref: str
    vessel_registration_ref: str
    role_permission_state: GateStatus
    provenance_hash: str = Field(min_length=12)


class AssertionOperationsControlRecord(SeaTraceModel):
    scenario_id: str
    assertion_operations_key: str
    private_assertion_ref: str
    crew_notes_ref: str
    hold_map_detail_ref: str
    exception_notes_ref: str
    role_permission_state: GateStatus
    provenance_hash: str = Field(min_length=12)


class CommercialLedgerControlRecord(SeaTraceModel):
    scenario_id: str
    commercial_ledger_key: str
    private_invoice_ref: str
    customer_terms_ref: str
    unit_price_ref: str
    margin_ref: str
    role_permission_state: GateStatus
    provenance_hash: str = Field(min_length=12)
