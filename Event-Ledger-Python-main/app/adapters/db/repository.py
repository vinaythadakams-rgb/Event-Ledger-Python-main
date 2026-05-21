from __future__ import annotations
from decimal import Decimal

from sqlalchemy import asc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.adapters.db.models import Event as EventModel
from app.core.exceptions import ConflictError
from app.domain.event import EventEntity
from app.domain.repository import EventRepositoryInterface


class SqlAlchemyEventRepository(EventRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_event(self, event: EventEntity) -> EventEntity:
        event_model = EventModel(
            event_id=event.event_id,
            account_id=event.account_id,
            type=event.type,
            amount=event.amount,
            currency=event.currency,
            event_timestamp=event.event_timestamp,
            event_metadata=event.metadata,
        )
        self.db.add(event_model)
        try:
            self.db.commit()
            self.db.refresh(event_model)
            return self._to_entity(event_model)
        except IntegrityError:
            self.db.rollback()
            existing = self.get_event_by_id(event.event_id)
            if existing:
                return existing
            raise ConflictError("Event with this eventId already exists")

    def get_event_by_id(self, event_id: str) -> EventEntity | None:
        statement = select(EventModel).where(EventModel.event_id == event_id)
        result = self.db.execute(statement).scalar_one_or_none()
        return self._to_entity(result) if result else None

    def list_events_for_account(self, account_id: str, limit: int = 100, offset: int = 0) -> list[EventEntity]:
        statement = (
            select(EventModel)
            .where(EventModel.account_id == account_id)
            .order_by(asc(EventModel.event_timestamp))
            .limit(limit)
            .offset(offset)
        )
        result = self.db.execute(statement).scalars().all()
        return [self._to_entity(event) for event in result]

    def compute_balance(self, account_id: str) -> Decimal:
        credit_query = select(func.coalesce(func.sum(EventModel.amount), 0)).where(
            EventModel.account_id == account_id,
            EventModel.type == "CREDIT",
        )
        debit_query = select(func.coalesce(func.sum(EventModel.amount), 0)).where(
            EventModel.account_id == account_id,
            EventModel.type == "DEBIT",
        )

        credit_total = self.db.execute(credit_query).scalar_one()
        debit_total = self.db.execute(debit_query).scalar_one()
        return Decimal(credit_total) - Decimal(debit_total)

    def _to_entity(self, model: EventModel) -> EventEntity:
        return EventEntity(
            event_id=model.event_id,
            account_id=model.account_id,
            type=model.type,
            amount=model.amount,
            currency=model.currency,
            event_timestamp=model.event_timestamp,
            metadata=model.event_metadata,
        )
