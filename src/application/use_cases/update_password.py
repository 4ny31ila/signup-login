from src.domain.user_repository import UserRepository
from passlib.context import CryptContext

class UpdatePasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, user_id: int, new_password: str) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.hashed_password = self.pwd_context.hash(new_password)
        self.user_repository.update(user)
