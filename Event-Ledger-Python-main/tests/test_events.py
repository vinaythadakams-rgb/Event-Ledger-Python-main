import pytest

from datetime import datetime

EVENT_PAYLOAD = {
    "eventId": "evt-001",
    "accountId": "acct-123",
    "type": "CREDIT",
    "amount": 150.00,
    "currency": "USD",
    "eventTimestamp": "2026-05-15T14:02:11Z",
    "metadata": {"source": "mainframe-batch", "batchId": "B-9042"},
}


def test_create_event_success(client):
    response = client.post("/events", json=EVENT_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["eventId"] == EVENT_PAYLOAD["eventId"]
    assert data["accountId"] == EVENT_PAYLOAD["accountId"]
    assert data["metadata"]["source"] == "mainframe-batch"


def test_get_event_by_id_success(client):
    client.post("/events", json=EVENT_PAYLOAD)

    response = client.get(f"/events/{EVENT_PAYLOAD['eventId']}")
    assert response.status_code == 200
    data = response.json()
    assert data["eventId"] == EVENT_PAYLOAD["eventId"]
    assert data["accountId"] == EVENT_PAYLOAD["accountId"]


def test_duplicate_event_submission_returns_existing(client):
    first = client.post("/events", json=EVENT_PAYLOAD)
    assert first.status_code == 201

    duplicate = client.post("/events", json=EVENT_PAYLOAD)
    assert duplicate.status_code == 201
    assert duplicate.json()["eventId"] == EVENT_PAYLOAD["eventId"]


def test_out_of_order_event_arrival(client):
    events = [
        {
            "eventId": "evt-003",
            "accountId": "acct-123",
            "type": "DEBIT",
            "amount": 20.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-16T15:00:00Z",
        },
        {
            "eventId": "evt-002",
            "accountId": "acct-123",
            "type": "CREDIT",
            "amount": 100.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-14T09:30:00Z",
        },
    ]

    for payload in events:
        response = client.post("/events", json=payload)
        assert response.status_code == 201

    list_response = client.get("/events", params={"account": "acct-123"})
    assert list_response.status_code == 200
    listed_events = list_response.json()
    assert [item["eventId"] for item in listed_events] == ["evt-002", "evt-003"]


def test_list_events_pagination(client):
    events = [
        {
            "eventId": "evt-004",
            "accountId": "acct-123",
            "type": "CREDIT",
            "amount": 10.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-13T08:00:00Z",
        },
        {
            "eventId": "evt-005",
            "accountId": "acct-123",
            "type": "CREDIT",
            "amount": 20.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-14T08:00:00Z",
        },
        {
            "eventId": "evt-006",
            "accountId": "acct-123",
            "type": "DEBIT",
            "amount": 5.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T08:00:00Z",
        },
    ]

    for payload in events:
        response = client.post("/events", json=payload)
        assert response.status_code == 201

    paginated_response = client.get("/events", params={"account": "acct-123", "limit": 1, "offset": 1})
    assert paginated_response.status_code == 200
    listed_events = paginated_response.json()
    assert len(listed_events) == 1
    assert listed_events[0]["eventId"] == "evt-005"


def test_validation_failure_missing_required_field(client):
    invalid = EVENT_PAYLOAD.copy()
    invalid.pop("accountId")

    response = client.post("/events", json=invalid)
    assert response.status_code == 422
    assert response.json()["detail"]


def test_get_event_not_found_returns_404(client):
    response = client.get("/events/non-existent")
    assert response.status_code == 404
