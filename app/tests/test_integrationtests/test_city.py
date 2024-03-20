from .fixtures import user_admin, user_admin_access_token, user, user_access_token, city, region


def test_success_return_status_code_201_create_city(client, user_admin_access_token, user, region) -> None:
    test_client, test_session = client

    response = test_client.post(
        "api/v1/location/city",
        json={
            "name": "Lodz",
            "region_id": str(region.id),
        },
        headers={"Authorization": f"Bearer {user_admin_access_token}"}
    )
    assert response.status_code == 201


def test_error_return_status_code_400_create_city_already_exists(client, user_admin_access_token, user, region) -> None:
    test_client, test_session = client

    response = test_client.post(
        "api/v1/location/city",
        json={
            "name": "Lodz",
            "region_id": str(region.id),
        },
        headers={"Authorization": f"Bearer {user_admin_access_token}"}
    )
    assert response.status_code == 201


def test_error_return_status_code_401_create_city_without_authorization(client, user, region) -> None:
    test_client, test_session = client

    response = test_client.post(
        "api/v1/location/city",
        json={
            "name": "Lodz",
            "region_id": str(region.id),
        },
    )
    assert response.status_code == 401


def test_error_return_status_code_401_create_city_with_invalid_authorization(
        client,
        user,
        region,
        user_access_token
) -> None:
    test_client, test_session = client

    response = test_client.post(
        "api/v1/location/city",
        json={
            "name": "Lodz",
            "region_id": str(region.id),
        },
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403


def test_success_return_status_code_200_get_cities_by_region_id(client, region, city) -> None:
    test_client, test_session = client

    response = test_client.get(
        f"api/v1/location/city/region/{region.id}",
    )
    assert response.status_code == 200


def test_success_return_status_code_200_get_cities(client, region, city) -> None:
    test_client, test_session = client

    response = test_client.get(
        "api/v1/location/city",
    )
    assert response.status_code == 200


def test_success_return_status_code_204_delete_city(client, user_admin_access_token, city) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"api/v1/location/city/{city.id}",
        headers={"Authorization": f"Bearer {user_admin_access_token}"}
    )
    assert response.status_code == 204


def test_error_return_status_code_401_delete_city_without_authorization(client, city) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"api/v1/location/city/{city.id}",
    )
    assert response.status_code == 401


def test_error_return_status_code_401_delete_city_with_invalid_authorization(
        client,
        city,
        user,
        user_access_token
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f"api/v1/location/city/{city.id}",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403


def test_success_return_status_code_200_update_city(client, city, user_admin_access_token) -> None:

    test_client, test_session = client

    response = test_client.put(
        f"api/v1/location/city/{city.id}",
        json={
            "name": "Lodz",
            "region_id": str(city.region_id),
        },
        headers={"Authorization": f"Bearer {user_admin_access_token}"}
    )
    assert response.status_code == 200


def test_error_return_status_code_401_update_city_without_authorization(client, city) -> None:
    test_client, test_session = client

    response = test_client.put(
        f"api/v1/location/city/{city.id}",
        json={
            "name": "Lodz",
        },
    )
    assert response.status_code == 401
