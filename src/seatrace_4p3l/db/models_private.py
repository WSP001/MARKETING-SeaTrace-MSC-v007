from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from seatrace_4p3l.db.session import Base


class PermissionedControlRow(Base):
    __tablename__ = "permissioned_controls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(String(80), index=True)
    control_type: Mapped[str] = mapped_column(String(80))
    control_ref: Mapped[str] = mapped_column(String(120), index=True)
    role_permission_state: Mapped[str] = mapped_column(String(40))
