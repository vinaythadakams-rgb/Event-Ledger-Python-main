# Event Ledger API

A production-ready Event Ledger API built with Python, FastAPI, SQLAlchemy, SQLite, and Pydantic.

## Features

- Accepts transaction events from multiple upstream systems
- Handles out-of-order and duplicate event delivery
- Idempotent event ingestion by `eventId`
- Chronological event listing by `eventTimestamp`
- Accurate balance computation per account
- Clean architecture with domain entities, repository interfaces, database adapters, and service use cases
- Global exception handling and structured logging
- OpenAPI documentation supported by FastAPI

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### POST /events

Submit a transaction event.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "evt-001",
    "accountId": "acct-123",
    "type": "CREDIT",
    "amount": 150.00,
    "currency": "USD",
    "eventTimestamp": "2026-05-15T14:02:11Z",
    "metadata": {
      "source": "mainframe-batch",
      "batchId": "B-9042"
    }
  }'
```

### GET /events/{id}

Retrieve a single event by `eventId`.

### GET /events?account={accountId}

List events for an account ordered by `eventTimestamp`.
Supports pagination with `limit` and `offset` query parameters.

### GET /accounts/{accountId}/balance

Return account balance, computed as `sum(CREDIT) - sum(DEBIT)`.

## Tests

Run the test suite with:

```bash
pytest
```

## Docker

Build and run the API in a container:

```bash
docker compose up --build
```

The API will be available at `http://127.0.0.1:8000` and the OpenAPI docs at `http://127.0.0.1:8000/docs`.

## Notes

- The SQLite database file is created automatically as `event_ledger.db`.
- Duplicate `eventId` submissions return the original event and do not create a new record.
- Event listing supports pagination with `limit` and `offset` query parameters.
- OpenAPI docs are available at `/docs`.
- Event ordering and balance calculation are correct regardless of ingestion order.
- Concurrent POSTs for the same `eventId` are protected by the database unique constraint and handled by the repository to return the existing event instead of creating a duplicate.
