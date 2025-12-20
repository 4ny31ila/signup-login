import jwt
import datetime
import os
from src.domain.user_repository import UserRepository
from passlib.context import CryptContext

# Load the secret key from an environment variable for security
SECRET_KEY = os.environ.get("SECRET_KEY", "a_default_secret_for_development")

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)

        if not user or not self.pwd_context.verify(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        payload = {
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token
