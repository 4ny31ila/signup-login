import pytest
from unittest.mock import MagicMock
from src.application.use_cases.delete_user import DeleteUserUseCase
from src.domain.user import User

def test_delete_user_success():
    # Arrange
    mock_user_repo = MagicMock()
    user = User(id=1, username="testuser", email="test@example.com", hashed_password="hashed")
    mock_user_repo.get_by_id.return_value = user

    delete_user_case = DeleteUserUseCase(mock_user_repo)

    # Act
    delete_user_case.execute(user_id=1)

    # Assert
    mock_user_repo.get_by_id.assert_called_with(1)
    mock_user_repo.delete.assert_called_with(1)

def test_delete_user_not_found():
    # Arrange
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id.return_value = None

    delete_user_case = DeleteUserUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found"):
        delete_user_case.execute(user_id=999)
