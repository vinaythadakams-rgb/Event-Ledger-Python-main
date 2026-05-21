def test_account_balance_computation_after_multiple_events(client):
    client.post(
        "/events",
        json={
            "eventId": "evt-b1",
            "accountId": "acct-balance",
            "type": "CREDIT",
            "amount": 100.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-10T10:00:00Z",
        },
    )
    client.post(
        "/events",
        json={
            "eventId": "evt-b2",
            "accountId": "acct-balance",
            "type": "DEBIT",
            "amount": 40.25,
            "currency": "USD",
            "eventTimestamp": "2026-05-11T12:00:00Z",
        },
    )
    client.post(
        "/events",
        json={
            "eventId": "evt-b3",
            "accountId": "acct-balance",
            "type": "CREDIT",
            "amount": 10.00,
            "currency": "USD",
            "eventTimestamp": "2026-05-09T08:00:00Z",
        },
    )

    response = client.get("/accounts/acct-balance/balance")
    assert response.status_code == 200
    assert response.json()["balance"] == 69.75
