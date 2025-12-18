from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
