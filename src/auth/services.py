from src.auth.domain import UserModel, UserNotFound
from src.auth.repository.user_db_repository import UserRepository
import bcrypt


class PasswordService:
    @staticmethod
    def protect_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(plain_password, protected_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), protected_password.encode('utf-8'))


class UserService:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    def create(self, user: UserModel) -> UserModel:
        user.password = self.password_service.protect_password(user.password)
        return self.user_repository.create(user)

    def get_user_by_code(self, user_code: str) -> UserModel:
        user = self.user_repository.get_user_by_code(user_code)
        if not user:
            raise UserNotFound(f"User with code {user_code} not found")
        return user

    def update(self, updated_user: UserModel) -> UserModel:
        return self.user_repository.update(updated_user.code, updated_user)

    def delete(self, user_code: str) -> None:
        self.user_repository.delete(user_code)
