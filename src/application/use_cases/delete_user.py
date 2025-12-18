from src.domain.user_repository import UserRepository

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        self.user_repository.delete(user_id)
