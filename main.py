import os
from werkzeug.serving import run_simple
from src.infrastructure.database.postgres_user_repository import PostgresUserRepository
from src.interfaces.web.server import create_app

# --- Dependency Injection Container ---

class DiContainer:
    def __init__(self):
        self.db_uri = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
        self.user_repo = PostgresUserRepository(self.db_uri)

    def get_use_case(self, use_case_class):
        """
        A simple factory to create use cases with their dependencies.
        """
        if hasattr(use_case_class, "__init__"):
            # Get the parameter names for the use case's constructor
            init_params = use_case_class.__init__.__code__.co_varnames

            # Basic dependency mapping
            dependencies = {}
            if 'user_repository' in init_params:
                dependencies['user_repository'] = self.user_repo

            return use_case_class(**dependencies)
        else:
            return use_case_class()

# --- Main Application Runner ---

def main():
    container = DiContainer()

    # The use case factory is passed to the web application
    app = create_app(container.get_use_case)

    print("Starting server on http://localhost:8080")
    run_simple('localhost', 8080, app)

if __name__ == '__main__':
    main()
