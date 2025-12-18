from typing import Optional
from src.domain.user import User
from src.domain.user_repository import UserRepository

class GetUserProfileUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> Optional[User]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
