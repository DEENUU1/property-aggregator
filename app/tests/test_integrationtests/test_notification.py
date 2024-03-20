from .fixtures import (
    user,
    notification,
    notification_filter,
    user_admin,
    user_admin_access_token,
    offer,
    region,
    city,
    user_access_token
)


def test_success_return_status_code_201_create_filter(client, user, user_access_token) -> None:
    test_client, test_session = client

    response = test_client.post(
        '/api/v1/notification/filter',
        json={"user_id": str(user.id), "category": "Mieszkanie"},
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 201


def test_error_return_status_code_401_create_filter_annonymous_user(client) -> None:
    test_client, test_session = client

    response = test_client.post(
        '/api/v1/notification/filter',
        json={"user_id": "1", "category": "Mieszkanie"}
    )
    assert response.status_code == 401


def test_success_return_status_code_200_update_status(client, user, user_access_token, notification_filter) -> None:
    test_client, test_session = client

    response = test_client.put(
        f'/api/v1/notification/filter/{notification_filter.id}',
        json={"status": True},
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 200


def test_error_return_status_code_401_update_status_annonymous_user(client, notification_filter) -> None:
    test_client, test_session = client

    response = test_client.put(
        f'/api/v1/notification/filter/{notification_filter.id}',
        json={"status": True}
    )
    assert response.status_code == 401


def test_error_return_status_code_404_update_status_notification_filter_not_found(
        client,
        user,
        user_access_token
) -> None:
    test_client, test_session = client

    response = test_client.put(
        f'/api/v1/notification/filter/279dcf76-a100-48b2-9fd4-f891d5093f4c',
        json={"status": True},
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 404


def test_error_return_status_code_403_update_status_notification_filter_invalid_user(
        client,
        user_admin,
        user_admin_access_token,
        notification_filter
) -> None:
    test_client, test_session = client

    response = test_client.put(
        f'/api/v1/notification/filter/{notification_filter.id}',
        json={"status": True},
        headers={'Authorization': f'Bearer {user_admin_access_token}'}
    )
    assert response.status_code == 403


def test_success_return_status_code_204_delete_notification_filter(
        client,
        user,
        user_access_token,
        notification_filter
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/notification/filter/{notification_filter.id}',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 204


def test_error_return_status_code_404_delete_notification_filter_not_found(
        client,
        user,
        user_access_token,
        notification_filter
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/notification/filter/279dcf76-a100-48b2-9fd4-f891d5093f4c',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 404


def test_error_return_status_code_401_delete_notification_filter_annonymous_user(client, notification_filter) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/notification/filter/{notification_filter.id}'
    )
    assert response.status_code == 401


def test_error_return_status_code_403_delete_notification_filter_invalid_user(
        client,
        notification_filter,
        user_admin,
        user_admin_access_token
) -> None:
    test_client, test_session = client

    response = test_client.delete(
        f'/api/v1/notification/filter/{notification_filter.id}',
        headers={'Authorization': f'Bearer {user_admin_access_token}'}
    )
    assert response.status_code == 403


def test_success_return_status_code_200_get_all_by_user(client, user, user_access_token, notification_filter) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification/filter',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 200


def test_success_return_status_code_200_get_notifications_by_user(
        client,
        user,
        user_access_token,
        notification
) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 200


def test_error_return_status_code_401_get_notifications_by_user_annonymous_user(client) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification'
    )
    assert response.status_code == 401


def test_success_return_status_code_200_get_notification_by_user(client, user, user_access_token, notification) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification/{notification.id}',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 200


def test_error_return_status_code_404_get_notification_by_user_not_found(
        client,
        user,
        user_access_token,
        notification
) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification/279dcf76-a100-48b2-9fd4-f891d5093f4c',
        headers={'Authorization': f'Bearer {user_access_token}'}
    )
    assert response.status_code == 404


def test_error_return_status_code_401_get_notification_by_user_annonymous_user(client, notification) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification/{notification.id}'
    )
    assert response.status_code == 401


def test_error_return_status_code_401_get_unread_user_count_annonymous_user(client) -> None:
    test_client, test_session = client

    response = test_client.get(
        f'/api/v1/notification/unread'
    )
    assert response.status_code == 401

