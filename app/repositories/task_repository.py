from datetime import date

from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, task_id: int):

        return self.session.get(
            Task,
            task_id
        )

    def get_all(self):

        return (
            self.session
            .query(Task)
            .all()
        )

    def create(self, task: Task):

        self.session.add(task)

        self.session.commit()

        self.session.refresh(task)

        return task

    def update(self):
        self.session.commit()

    def delete(self, task_id: int):

        task = self.get_by_id(task_id)

        if task:

            self.session.delete(task)

            self.session.commit()

        return task

    def get_tasks_by_user(
        self,
        user_id: int
    ):

        return (
            self.session
            .query(Task)
            .filter(
                Task.user_id == user_id
            )
            .all()
        )

    def get_tasks_by_date(
        self,
        user_id: int,
        target_date: date
    ):

        return (
            self.session
            .query(Task)
            .filter(
                Task.user_id == user_id,
                Task.datum == target_date
            )
            .all()
        )
