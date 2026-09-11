from __future__ import annotations

from sqlalchemy.orm import Session

from seatrace_4p3l.db.models_private import PermissionedControlRow
from seatrace_4p3l.db.models_public import PublicPacketRow


def save_public_packet(session: Session, row: PublicPacketRow) -> PublicPacketRow:
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def save_permissioned_control(session: Session, row: PermissionedControlRow) -> PermissionedControlRow:
    session.add(row)
    session.commit()
    session.refresh(row)
    return row
