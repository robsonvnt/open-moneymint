from datetime import date

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

from src.auth.domain import UserNotFound, UserModel
from src.investment.helpers import generate_code

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


def to_database(user_model: UserModel) -> User:
    return User(**user_model.model_dump())


def to_model(user: User) -> UserModel:
    return UserModel(**user.to_dict())


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserModel):
        user.code = generate_code()
        user.created_at = date.today()
        db_user = to_database(user)
        self.session.add(db_user)
        self.session.commit()
        return to_model(db_user)

    def get_user_by_code(self, user_code: str):
        try:
            user = self.session.query(User).filter(User.code == user_code).one()
            return to_model(user)
        except NoResultFound:
            raise UserNotFound(f"User with code {user_code} not found")

    def get_user_by_login(self, login: str):
        try:
            user = self.session.query(User).filter(User.login == login).one()
            return to_model(user)
        except NoResultFound:
            raise UserNotFound(f"User with login {login} not found")

    def update(self, user_code: int, updated_user: UserModel):
        try:
            user = self.session.query(User).filter(User.code == user_code).one()
            for key, value in updated_user.model_dump().items():
                setattr(user, key, value)
            self.session.commit()
            return to_model(user)
        except NoResultFound:
            raise UserNotFound(f"User with code {user_code} not found")

    def delete(self, user_code: str):
        try:
            user = self.session.query(User).filter(User.code == user_code).one()
            self.session.delete(user)
            self.session.commit()
        except NoResultFound:
            raise UserNotFound(f"User with code {user_code} not found")

