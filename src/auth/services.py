from src.auth.domain import User
from src.auth.repository.user_db_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        return self.user_repository.add_user(user)

    def get_user_by_code(self, user_code: str) -> User:
        user = self.user_repository.get_user_by_code(user_code)
        if not user:
            raise UserNotFound(f"User with code {user_code} not found")
        return user

    def update_user(self, user_code: str, updated_data: dict) -> User:
        user = self.user_repository.get_user_by_code(user_code)
        if not user:
            raise UserNotFound(f"User with code {user_code} not found")
        return self.user_repository.update_user(user_code, updated_data)

    def delete_user(self, user_code: str) -> None:
        user = self.user_repository.get_user_by_code(user_code)
        if not user:
            raise UserNotFound(f"User with code {user_code} not found")
        self.user_repository.delete_user(user.id)
