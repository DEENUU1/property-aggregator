from .fixtures import user_admin_access_token, user, user_access_token, city, region, offer, offer_data


def test_success_return_status_code_201_create_offer(client, user_admin_access_token, city, region) -> None:
    test_client, test_session = client

    response = test_client.post(
        "/api/v1/offer",
        json=offer_data,
        headers={"Authorization": f"Bearer {user_admin_access_token}"},
    )
    assert response.status_code == 201


def test_error_return_status_code_400_create_offer_already_exists(client, city, region, offer) -> None:
    test_client, test_session = client

    response = test_client.post(
        "/api/v1/offer",
        json=offer_data,
    )
    assert response.status_code == 400


def test_success_return_status_code_204_delete_offer(client, user_admin_access_token, offer) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"/api/v1/offer/{offer.id}",
        headers={"Authorization": f"Bearer {user_admin_access_token}"},
    )
    assert response.status_code == 204


def test_error_return_status_code_404_delete_offer_not_found(client, user_admin_access_token) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"/api/v1/offer/279dcf76-a100-48b2-9fd4-f891d5093f4c",
        headers={"Authorization": f"Bearer {user_admin_access_token}"},
    )
    assert response.status_code == 404


def test_error_return_status_code_401_delete_offer_unauthorized(client, offer) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"/api/v1/offer/{offer.id}",
    )
    assert response.status_code == 401


def test_error_return_status_code_403_delete_offer_user(client, offer, user, user_access_token) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"/api/v1/offer/{offer.id}",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    assert response.status_code == 403


def test_success_return_status_code_200_get_offers(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer",
    )
    assert response.status_code == 200


def test_success_return_status_code_200_get_offer_valid_params(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?page=1&page_size=15&category=Mieszkanie&subcategory=Wynajem&floor=1",
    )
    assert response.status_code == 200


def test_error_return_status_code_422_get_offer_page_number_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?page=-1",
    )
    assert response.status_code == 422


def test_error_return_status_code_422_get_offer_price_min_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?price_min=-1",
    )
    assert response.status_code == 422


def test_error_return_status_code_422_get_offer_price_max_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?price_max=-1",
    )
    assert response.status_code == 422


def test_error_return_status_code_422_get_offer_area_min_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?area_min=-1",
    )
    assert response.status_code == 422


def test_error_return_status_code_422_get_offer_area_max_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?area_max=-1",
    )
    assert response.status_code == 422

def test_error_return_status_code_422_get_offer_rooms_lower_than_zero(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        "/api/v1/offer?rooms=-1",
    )
    assert response.status_code == 422


def test_success_return_status_code_200_get_offer(client, offer) -> None:
    test_client, test_session = client

    response = test_client.get(
        f"/api/v1/offer/{offer.id}",
    )
    assert response.status_code == 200


def test_error_return_status_code_404_get_offer_not_found(client) -> None:
    test_client, test_session = client

    response = test_client.get(
        f"/api/v1/offer/279dcf76-a100-48b2-9fd4-f891d5093f4c",
    )
    assert response.status_code == 404
