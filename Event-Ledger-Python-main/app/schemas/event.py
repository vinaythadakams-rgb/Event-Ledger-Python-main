from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, condecimal

class EventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    eventId: str = Field(..., min_length=1)
    accountId: str = Field(..., min_length=1)
    type: Literal["CREDIT", "DEBIT"]
    amount: condecimal(gt=0, max_digits=14, decimal_places=2)
    currency: str = Field(..., min_length=1)
    eventTimestamp: datetime
    metadata: dict[str, str] | None = Field(default=None)

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    pass

class BalanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    accountId: str
    balance: float
