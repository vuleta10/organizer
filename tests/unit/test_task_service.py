from datetime import date

from app.models.task import Task
from app.models.user import User

from app.services.task_service import TaskService


class MockUserRepository:

    def get_by_id(self, user_id):

        return User(
            id=user_id,
            username="igor",
            password="123"
        )


class MockTaskRepository:

    def __init__(self):

        self.tasks = []

    def create(self, task):

        task.id = len(self.tasks) + 1

        self.tasks.append(task)

        return task

    def get_tasks_by_user(
        self,
        user_id
    ):

        return [
            task
            for task in self.tasks
            if task.user_id == user_id
        ]

    def get_tasks_by_date(
        self,
        user_id,
        task_date
    ):

        return [
            task
            for task in self.tasks
            if task.user_id == user_id
            and task.datum == task_date
        ]

    def get_by_id(self, task_id):

        for task in self.tasks:

            if task.id == task_id:
                return task

        return None

    def update(self):
        pass

    def delete(self, task_id):

        task = self.get_by_id(task_id)

        if task:
            self.tasks.remove(task)

        return task


def test_create_task():

    service = TaskService(
        MockTaskRepository(),
        MockUserRepository()
    )

    task = service.create_task(
        1,
        "Study SQLAlchemy",
        date.today()
    )

    assert task.id == 1


def test_get_tasks_by_user():

    task_repo = MockTaskRepository()

    service = TaskService(
        task_repo,
        MockUserRepository()
    )

    service.create_task(
        1,
        "Task 1",
        date.today()
    )

    service.create_task(
        1,
        "Task 2",
        date.today()
    )

    tasks = service.get_tasks_by_user(1)

    assert len(tasks) == 2


def test_get_tasks_by_date():

    task_repo = MockTaskRepository()

    service = TaskService(
        task_repo,
        MockUserRepository()
    )

    today = date.today()

    service.create_task(
        1,
        "Task",
        today
    )

    tasks = service.get_tasks_by_date(
        1,
        today
    )

    assert len(tasks) == 1


def test_update_task():

    task_repo = MockTaskRepository()

    service = TaskService(
        task_repo,
        MockUserRepository()
    )

    created = service.create_task(
        1,
        "Old Task",
        date.today()
    )

    updated = service.update_task(
        created.id,
        "New Task",
        date.today(),
        True
    )

    assert updated.task == "New Task"
    assert updated.done is True


def test_delete_task():

    task_repo = MockTaskRepository()

    service = TaskService(
        task_repo,
        MockUserRepository()
    )

    task = service.create_task(
        1,
        "Task",
        date.today()
    )

    service.delete_task(task.id)

    assert len(task_repo.tasks) == 0