from __future__ import annotations

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from seatrace_4p3l.db.session import Base


class PublicPacketRow(Base):
    __tablename__ = "public_packets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(String(80), index=True)
    packet_type: Mapped[str] = mapped_column(String(80))
    spine_id: Mapped[str] = mapped_column(String(120), index=True)
    state_label: Mapped[str] = mapped_column(String(120))
    variance_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
