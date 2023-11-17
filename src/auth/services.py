from datetime import timedelta, datetime
from typing import Optional
import jwt

from src.auth.domain.auth_erros import ExpiredToken, InvalidToken
from src.auth.domain.models import UserModel
from src.auth.domain.user_erros import UserNotFound
from src.auth.repository.user_db_repository import UserRepository
import bcrypt


class PasswordService:
    @staticmethod
    def protect_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(plain_password, protected_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), protected_password.encode('utf-8'))


class AuthenticationUserService:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService, secret_key: str):
        self.user_repository = user_repository
        self.password_service = password_service
        self.SECRET_KEY = secret_key
        self.ALGORITHM = "HS256"

    def authenticate_user(self, user_name: str, password: str) -> UserModel:
        user = self.user_repository.get_by_user_name(user_name)
        is_password_valid = self.password_service.verify_password(password, user.password)
        match is_password_valid:
            case True:
                return user
            case False:
                raise UserNotFound(f"User with login {user_name} not found")

    def create_access_token(self, user: UserModel, expires_delta: Optional[timedelta] = None):
        data = {"user_name": user.user_name}
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_username_from_access_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return decoded_token["user_name"]
        except jwt.ExpiredSignatureError:
            raise ExpiredToken()
        except jwt.InvalidTokenError:
            raise InvalidToken()



class UserService:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    def create(self, user: UserModel) -> UserModel:
        user.password = self.password_service.protect_password(user.password)
        return self.user_repository.create(user)

    def get_user_by_code(self, user_code: str) -> UserModel:
        user = self.user_repository.get_user_by_code(user_code)
        return user

    def update(self, updated_user: UserModel) -> UserModel:
        return self.user_repository.update(updated_user.code, updated_user)

    def delete(self, user_code: str) -> None:
        self.user_repository.delete(user_code)


class UserServiceFactory:
    @staticmethod
    def create_investment_service(db_session) -> UserService:
        return UserService(UserRepository(db_session), PasswordService())
