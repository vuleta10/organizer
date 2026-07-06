from app.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository


ALL_TEST_USERNAMES = [f"utest{i}" for i in range(1, 9)]

PRECREATED_USERNAMES = [f"utest{i}" for i in range(2, 9)]

TEST_PASSWORD = "test123"


def _delete_test_user(session, username):

    user_repo = UserRepository(session)
    task_repo = TaskRepository(session)

    user = user_repo.get_by_username(username)

    if not user:
        return

    for task in task_repo.get_tasks_by_user(user.id):
        task_repo.delete(task.id)

    user_repo.delete(user.id)


def test_delete_existing_test_users():

    session = SessionLocal()

    try:

        for username in ALL_TEST_USERNAMES:
            _delete_test_user(session, username)

    finally:
        session.close()

    session = SessionLocal()

    try:

        user_repo = UserRepository(session)

        for username in ALL_TEST_USERNAMES:
            assert user_repo.get_by_username(username) is None

    finally:
        session.close()


def test_create_test_users(client):

    for username in PRECREATED_USERNAMES:

        response = client.post(
            "/users/register",
            json={
                "username": username,
                "password": TEST_PASSWORD
            }
        )

        assert response.status_code == 201
