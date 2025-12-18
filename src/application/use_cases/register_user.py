from src.domain.user import User
from src.domain.user_repository import UserRepository
from passlib.context import CryptContext

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, username: str, email: str, password: str) -> User:
        # Check if user already exists
        if self.user_repository.get_by_email(email):
            raise ValueError("User with this email already exists.")

        hashed_password = self.pwd_context.hash(password)

        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        self.user_repository.add(new_user)

        return self.user_repository.get_by_email(email)
