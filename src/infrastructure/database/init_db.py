import os
from sqlalchemy import create_engine, MetaData
from src.infrastructure.database.postgres_user_repository import PostgresUserRepository

# It's recommended to load this from environment variables or a config file
DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")

def setup_database():
    """
    Creates the 'users' table in the database if it doesn't exist.
    """
    print("Setting up the database...")
    try:
        # We instantiate the repository just to get access to its metadata
        repo = PostgresUserRepository(DATABASE_URI)
        engine = repo.engine
        metadata = repo.metadata

        # Create all tables defined in the metadata
        metadata.create_all(engine)

        print("Database table 'users' created or already exists.")
    except Exception as e:
        print(f"An error occurred during database setup: {e}")

if __name__ == "__main__":
    # This allows the script to be run directly to set up the database
    setup_database()
