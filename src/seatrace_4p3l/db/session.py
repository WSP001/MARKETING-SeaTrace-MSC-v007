from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


def database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///./seatrace_4p3l.local.db")


def build_session_factory() -> sessionmaker[Session]:
    engine = create_engine(database_url())
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
