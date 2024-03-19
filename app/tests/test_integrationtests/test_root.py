def test_success_health(client) -> None:
    test_client, _ = client

    response = test_client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
