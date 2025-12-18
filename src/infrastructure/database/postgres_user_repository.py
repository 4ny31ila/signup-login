from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from typing import Optional
from src.domain.user import User
from src.domain.user_repository import UserRepository

class PostgresUserRepository(UserRepository):
    def __init__(self, database_uri: str):
        self.engine = create_engine(database_uri)
        self.metadata = MetaData()
        self.users = Table('users', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('username', String(50), nullable=False),
            Column('email', String(100), unique=True, nullable=False),
            Column('hashed_password', String(255), nullable=False)
        )

    def _map_row_to_user(self, row) -> Optional[User]:
        if row is None:
            return None
        return User(
            id=row.id,
            username=row.username,
            email=row.email,
            hashed_password=row.hashed_password
        )

    def add(self, user: User) -> None:
        query = self.users.insert().values(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        with self.engine.connect() as connection:
            connection.execute(query)
            connection.commit()


    def get_by_id(self, user_id: int) -> Optional[User]:
        query = self.users.select().where(self.users.c.id == user_id)
        with self.engine.connect() as connection:
            result = connection.execute(query).fetchone()
            return self._map_row_to_user(result)

    def get_by_email(self, email: str) -> Optional[User]:
        query = self.users.select().where(self.users.c.email == email)
        with self.engine.connect() as connection:
            result = connection.execute(query).fetchone()
            return self._map_row_to_user(result)

    def update(self, user: User) -> None:
        query = self.users.update().where(self.users.c.id == user.id).values(
            hashed_password=user.hashed_password
        )
        with self.engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete(self, user_id: int) -> None:
        query = self.users.delete().where(self.users.c.id == user_id)
        with self.engine.connect() as connection:
            connection.execute(query)
            connection.commit()
