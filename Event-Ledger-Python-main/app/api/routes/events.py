from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_event_service
from app.core.exceptions import ValidationError
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import EventService

router = APIRouter()

@router.post("/events", response_model=EventResponse, status_code=201)
def create_event(
    payload: EventCreate,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    try:
        return service.create_event(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.message)

@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: str, service: EventService = Depends(get_event_service)) -> EventResponse:
    return service.get_event(event_id)

@router.get("/events", response_model=list[EventResponse])
def list_events(
    account: str = Query(..., alias="account"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of events to return"),
    offset: int = Query(0, ge=0, description="Number of events to skip"),
    service: EventService = Depends(get_event_service),
) -> list[EventResponse]:
    return service.list_events(account, limit=limit, offset=offset)
