from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import accounts, events
from app.core.logging import setup_logging
from app.db.init_db import initialize_database
from app.middleware.errors import ExceptionHandlingMiddleware

setup_logging()

app = FastAPI(
    title="Event Ledger API",
    description="A robust event ledger for out-of-order and duplicate financial transaction events.",
    version="1.0.0",
)

app.add_middleware(ExceptionHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="", tags=["Events"])
app.include_router(accounts.router, prefix="", tags=["Accounts"])

initialize_database()
