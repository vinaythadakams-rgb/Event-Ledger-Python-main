from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal

from app.domain.event import EventEntity


class EventRepositoryInterface(ABC):
    @abstractmethod
    def create_event(self, event: EventEntity) -> EventEntity:
        raise NotImplementedError

    @abstractmethod
    def get_event_by_id(self, event_id: str) -> EventEntity | None:
        raise NotImplementedError

    @abstractmethod
    def list_events_for_account(self, account_id: str) -> list[EventEntity]:
        raise NotImplementedError

    @abstractmethod
    def compute_balance(self, account_id: str) -> Decimal:
        raise NotImplementedError
