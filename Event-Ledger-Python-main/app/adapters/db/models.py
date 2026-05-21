from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    account_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    type: Mapped[str] = mapped_column(Enum("CREDIT", "DEBIT", name="event_type"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    event_metadata: Mapped[dict[str, str] | None] = mapped_column(
        "metadata",
        MutableDict.as_mutable(JSON),
        nullable=True,
    )
