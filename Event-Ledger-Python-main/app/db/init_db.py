import logging

from app.db.base import Base
from app.db.session import engine

logger = logging.getLogger(__name__)

def initialize_database() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized")
    except Exception as exc:
        logger.exception("Failed to initialize database schema")
        raise
