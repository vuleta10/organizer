from app.models.user import User
from app.services.user_service import UserService


class MockUserRepository:

    def __init__(self):
        self.users = []

    def get_by_username(self, username):

        for user in self.users:
            if user.username == username:
                return user

        return None

    def create(self, user):

        user.id = len(self.users) + 1

        self.users.append(user)

        return user

    def update(self):
        pass


def test_register_success():

    repo = MockUserRepository()

    service = UserService(repo)

    user = service.register(
        "igor",
        "123"
    )

    assert user.username == "igor"


def test_register_duplicate_user():

    repo = MockUserRepository()

    repo.users.append(
        User(
            id=1,
            username="igor",
            password="123"
        )
    )

    service = UserService(repo)

    try:

        service.register(
            "igor",
            "456"
        )

        assert False

    except ValueError:
        assert True


def test_login_success():

    repo = MockUserRepository()

    repo.users.append(
        User(
            id=1,
            username="igor",
            password="123"
        )
    )

    service = UserService(repo)

    user = service.login(
        "igor",
        "123"
    )

    assert user.username == "igor"


def test_login_wrong_password():

    repo = MockUserRepository()

    repo.users.append(
        User(
            id=1,
            username="igor",
            password="123"
        )
    )

    service = UserService(repo)

    try:

        service.login(
            "igor",
            "999"
        )

        assert False

    except ValueError:
        assert True


def test_change_password():

    repo = MockUserRepository()

    repo.users.append(
        User(
            id=1,
            username="igor",
            password="123"
        )
    )

    service = UserService(repo)

    user = service.change_password(
        "igor",
        "123",
        "456"
    )

    assert user.password == "456"