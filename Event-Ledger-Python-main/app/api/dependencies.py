from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService


def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return EventRepository(db)


def get_event_service(repository: EventRepository = Depends(get_event_repository)) -> EventService:
    return EventService(repository)
