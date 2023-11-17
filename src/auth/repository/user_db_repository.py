from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

from src.auth.domain import UserNotFound
from src.constants import SUCCESS_RESULT

Base = declarative_base()


class User(Base, AllFeaturesMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    name = Column(String)
    login = Column(String, index=True, unique=True)
    password = Column(String)
    created_at = Column(Date)


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_code(self, user_code: str):
        try:
            return self.session.query(User).filter(User.code == user_code).one()
        except NoResultFound:
            raise UserNotFound(f"User with code {user_code} not found")

    def get_user_by_login(self, login: str):
        return self.session.query(User).filter(User.login == login).first()

    def update(self, user_code: int, updated_data: dict):
        try:
            user = self.session.query(User).filter(User.code == user_code).one()
            for key, value in updated_data.items():
                setattr(user, key, value)
            self.session.commit()
            return user
        except NoResultFound:
            raise UserNotFound(f"User with code {user_code} not found")

    def delete(self, user_code: str):
        user = self.get_user_by_code(user_code)
        self.session.delete(user)
        self.session.commit()
