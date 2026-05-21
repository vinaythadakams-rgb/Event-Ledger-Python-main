from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_URL = "sqlite:///./event_ledger.db"

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
