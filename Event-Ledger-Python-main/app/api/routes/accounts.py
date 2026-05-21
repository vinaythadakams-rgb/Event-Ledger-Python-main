from fastapi import APIRouter, Depends

from app.api.dependencies import get_event_service
from app.schemas.event import BalanceResponse
from app.services.event_service import EventService

router = APIRouter()

@router.get("/accounts/{account_id}/balance", response_model=BalanceResponse)
def get_balance(account_id: str, service: EventService = Depends(get_event_service)) -> BalanceResponse:
    return service.get_account_balance(account_id)
