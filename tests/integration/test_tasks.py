def _get_user_id(client, username):

    response = client.post(
        "/users/login",
        json={
            "username": username,
            "password": "test123"
        }
    )

    return response.get_json()["id"]


def test_create_task(client):

    user_id = _get_user_id(client, "utest5")

    response = client.post(
        "/tasks",
        json={
            "user_id": user_id,
            "task": "Learn Flask",
            "datum": "2026-07-10"
        }
    )

    assert response.status_code == 201

def test_get_user_tasks(client):

    user_id = _get_user_id(client, "utest6")

    client.post(
        "/tasks",
        json={
            "user_id": user_id,
            "task": "Task A",
            "datum": "2026-07-10"
        }
    )

    response = client.get(
        f"/tasks/user/{user_id}"
    )

    assert response.status_code == 200

    tasks = response.get_json()

    assert len(tasks) > 0

def test_get_tasks_by_date(client):

    user_id = _get_user_id(client, "utest7")

    client.post(
        "/tasks",
        json={
            "user_id": user_id,
            "task": "Task Date",
            "datum": "2026-07-15"
        }
    )

    response = client.get(
        f"/tasks/user/{user_id}/2026-07-15"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1

def test_delete_task(client):

    user_id = _get_user_id(client, "utest8")

    task_response = client.post(
        "/tasks",
        json={
            "user_id": user_id,
            "task": "Delete Me",
            "datum": "2026-07-20"
        }
    )

    task_id = (
        task_response
        .get_json()["id"]
    )

    response = client.delete(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 200
