from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

EventType = Literal["CREDIT", "DEBIT"]

@dataclass
class EventEntity:
    event_id: str
    account_id: str
    type: EventType
    amount: Decimal
    currency: str
    event_timestamp: datetime
    metadata: dict[str, str] | None = None
