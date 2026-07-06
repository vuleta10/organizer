def test_create_task(client):

    user_response = client.post(
        "/users/register",
        json={
            "username": "pera_task",
            "password": "123"
        }
    )

    user_id = (
        user_response
        .get_json()["id"]
    )

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

    user_response = client.post(
        "/users/register",
        json={
            "username": "user2",
            "password": "123"
        }
    )

    user_id = (
        user_response
        .get_json()["id"]
    )

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

    user_response = client.post(
        "/users/register",
        json={
            "username": "user3",
            "password": "123"
        }
    )

    user_id = (
        user_response
        .get_json()["id"]
    )

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

    user_response = client.post(
        "/users/register",
        json={
            "username": "deleteuser",
            "password": "123"
        }
    )

    user_id = (
        user_response
        .get_json()["id"]
    )

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
