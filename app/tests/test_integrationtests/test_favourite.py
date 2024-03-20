from .fixtures import user_access_token, user_admin_access_token, user, user_admin, favourite, offer, city, region


def test_success_return_status_code_201_create_favourite(
        client,
        user,
        user_access_token,
        region,
        city,
        offer
) -> None:
    test_client, test_session = client

    response = test_client.post(
        '/api/v1/favourite',
        headers={'Authorization': f'Bearer {user_access_token}'},
        json={'offer_id': str(offer.id)}
    )
    assert response.status_code == 201


def test_error_return_status_code_404_create_favourite_offer_not_found(
        client,
        user,
        user_access_token,
        region,
        city
) -> None:
    test_client, test_session = client

    response = test_client.post(
        '/api/v1/favourite',
        headers={'Authorization': f'Bearer {user_access_token}'},
        json={'offer_id': '279dcf76-a100-48b2-9fd4-f891d5093f4c'}
    )
    assert response.status_code == 404


def test_error_return_status_code_401_create_favourite_anonymous_user(
        client,
        region,
        city,
        offer,
) -> None:
    test_client, test_session = client

    response = test_client.post(
        '/api/v1/favourite',
        json={'offer_id': str(offer.id)}
    )
    assert response.status_code == 401


def test_success_return_status_code_204_delete_favourite(
        client,
        user,
        user_access_token,
        favourite
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/favourite/{favourite.id}',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 204


def test_error_return_status_code_404_delete_favourite_favourite_not_found(
        client,
        user,
        user_access_token,
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        '/api/v1/favourite/279dcf76-a100-48b2-9fd4-f891d5093f4c',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 404


def test_error_return_status_code_401_delete_favourite_anonymous_user(
        client,
        region,
        city,
        offer,
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/favourite/{offer.id}',
    )
    assert response.status_code == 401


def test_error_return_status_code_401_delete_favourite_invalid_user(
        client,
        user_admin,
        user_admin_access_token,
        favourite
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/favourite/{favourite.id}',
        headers={'Authorization': f'Bearer {user_admin_access_token}'}
    )
    assert response.status_code == 401


def test_success_return_status_code_200_get_all_by_user(
        client,
        user,
        user_access_token,
        favourite
) -> None:
    test_client, test_session = client

    response = test_client.get(
        "api/v1/favourite",
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 200


def test_error_return_status_code_401_get_all_by_user_anonymous_user(
        client,
        region,
        city,
        offer,
) -> None:
    test_client, test_session = client

    response = test_client.get(
        "api/v1/favourite",
    )
    assert response.status_code == 401

