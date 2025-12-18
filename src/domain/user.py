import dataclasses
from typing import Optional

@dataclasses.dataclass
class User:
    username: str
    email: str
    hashed_password: str
    id: Optional[int] = None
