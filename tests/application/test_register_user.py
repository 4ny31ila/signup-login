import pytest
from unittest.mock import MagicMock
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.user import User

def test_register_user_success(mocker):
    # Arrange
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_email.return_value = None  # No existing user

    # Mock the user that will be "created" and returned
    created_user = User(id=1, username="testuser", email="test@example.com", hashed_password="hashed_password")

    # When get_by_email is called after adding the user, return the created user
    mocker.patch.object(mock_user_repo, 'get_by_email', side_effect=[None, created_user])

    register_use_case = RegisterUserUseCase(mock_user_repo)

    # Act
    result = register_use_case.execute("testuser", "test@example.com", "password123")

    # Assert
    mock_user_repo.add.assert_called_once()
    assert result.email == "test@example.com"
    assert result.id == 1

def test_register_user_already_exists():
    # Arrange
    mock_user_repo = MagicMock()
    existing_user = User(id=1, username="existinguser", email="exists@example.com", hashed_password="hashed_password")
    mock_user_repo.get_by_email.return_value = existing_user

    register_use_case = RegisterUserUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="User with this email already exists."):
        register_use_case.execute("newuser", "exists@example.com", "password123")
