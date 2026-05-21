from decimal import Decimal
import logging

from app.core.exceptions import NotFoundError
from app.domain.event import EventEntity
from app.domain.repository import EventRepositoryInterface
from app.schemas.event import BalanceResponse, EventCreate, EventResponse

logger = logging.getLogger(__name__)

class EventService:
    def __init__(self, repository: EventRepositoryInterface) -> None:
        self.repository = repository

    def _map_entity(self, event: EventEntity) -> EventResponse:
        return EventResponse.model_validate(
            {
                "eventId": event.event_id,
                "accountId": event.account_id,
                "type": event.type,
                "amount": event.amount,
                "currency": event.currency,
                "eventTimestamp": event.event_timestamp,
                "metadata": event.metadata,
            }
        )

    def _build_entity(self, payload: EventCreate) -> EventEntity:
        return EventEntity(
            event_id=payload.eventId,
            account_id=payload.accountId,
            type=payload.type,
            amount=payload.amount,
            currency=payload.currency,
            event_timestamp=payload.eventTimestamp,
            metadata=payload.metadata,
        )

    def create_event(self, payload: EventCreate) -> EventResponse:
        entity = self._build_entity(payload)
        event = self.repository.create_event(entity)
        logger.info("Processed event %s", payload.eventId)
        return self._map_entity(event)

    def get_event(self, event_id: str) -> EventResponse:
        event = self.repository.get_event_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found", details={"eventId": event_id})
        return self._map_entity(event)

    def list_events(self, account_id: str, limit: int = 100, offset: int = 0) -> list[EventResponse]:
        events = self.repository.list_events_for_account(account_id, limit=limit, offset=offset)
        return [self._map_entity(event) for event in events]

    def get_account_balance(self, account_id: str) -> BalanceResponse:
        balance = self.repository.compute_balance(account_id)
        return BalanceResponse(accountId=account_id, balance=float(balance))
