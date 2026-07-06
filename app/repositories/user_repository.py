from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int):
        return self.session.get(
            User,
            user_id
        )

    def get_all(self):
        return (
            self.session
            .query(User)
            .all()
        )

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update(self):
        self.session.commit()

    def delete(self, user_id: int):

        user = self.get_by_id(user_id)

        if user:
            self.session.delete(user)
            self.session.commit()

        return user

    def get_by_username(
        self,
        username: str
    ):
        return (
            self.session
            .query(User)
            .filter(
                User.username == username
            )
            .first()
        )
