

def test_success_register(client) -> None:

    response = client.post(
        "/api/v1/user/register",
        json={
            "email": "test@example.com",
            "password": "test",
            "username": "test",
        },
    )
    assert response.status_code == 201
