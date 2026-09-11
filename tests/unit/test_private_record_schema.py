from __future__ import annotations

from seatrace_4p3l.schemas.private_records import (
    AssertionOperationsControlRecord,
    CommercialLedgerControlRecord,
    IdentityAccessControlRecord,
)


def test_private_companion_records_validate_as_permissioned_refs():
    identity = IdentityAccessControlRecord(
        scenario_id="SCN-LOT-2026-PUB-01",
        identity_access_key="SCN-IDENTITY-KEY-01",
        private_identity_ref="PERMISSIONED-ID-REF",
        exact_gps_track_ref="PERMISSIONED-TRACK-REF",
        captain_ref="PERMISSIONED-CAPTAIN-REF",
        vessel_registration_ref="PERMISSIONED-VESSEL-REF",
        role_permission_state="PASS",
        provenance_hash="SCN-HASH-IDENTITY-001",
    )
    assertion = AssertionOperationsControlRecord(
        scenario_id="SCN-LOT-2026-PUB-01",
        assertion_operations_key="SCN-ASSERTION-KEY-01",
        private_assertion_ref="PERMISSIONED-ASSERTION-REF",
        crew_notes_ref="PERMISSIONED-CREW-REF",
        hold_map_detail_ref="PERMISSIONED-MAP-REF",
        exception_notes_ref="PERMISSIONED-EXCEPTION-REF",
        role_permission_state="PASS",
        provenance_hash="SCN-HASH-ASSERTION-001",
    )
    ledger = CommercialLedgerControlRecord(
        scenario_id="SCN-LOT-2026-PUB-01",
        commercial_ledger_key="SCN-COMMERCIAL-KEY-01",
        private_invoice_ref="PERMISSIONED-INVOICE-REF",
        customer_terms_ref="PERMISSIONED-TERMS-REF",
        unit_price_ref="PERMISSIONED-UNIT-REF",
        margin_ref="PERMISSIONED-MARGIN-REF",
        role_permission_state="PASS",
        provenance_hash="SCN-HASH-COMMERCIAL-001",
    )

    assert identity.role_permission_state == "PASS"
    assert assertion.role_permission_state == "PASS"
    assert ledger.role_permission_state == "PASS"
