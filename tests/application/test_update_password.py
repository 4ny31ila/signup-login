import pytest
from unittest.mock import MagicMock
from src.application.use_cases.update_password import UpdatePasswordUseCase
from src.domain.user import User

def test_update_password_success(mocker):
    # Arrange
    mock_user_repo = MagicMock()
    user = User(id=1, username="testuser", email="test@example.com", hashed_password="old_hashed")
    mock_user_repo.get_by_id.return_value = user

    # Mock the password hashing
    mocker.patch('passlib.context.CryptContext.hash', return_value="new_hashed_password")

    update_password_case = UpdatePasswordUseCase(mock_user_repo)

    # Act
    update_password_case.execute(user_id=1, new_password="new_password123")

    # Assert
    mock_user_repo.get_by_id.assert_called_with(1)
    mock_user_repo.update.assert_called_once()
    updated_user = mock_user_repo.update.call_args[0][0]
    assert updated_user.hashed_password == "new_hashed_password"

def test_update_password_user_not_found():
    # Arrange
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id.return_value = None

    update_password_case = UpdatePasswordUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found"):
        update_password_case.execute(user_id=999, new_password="new_password123")
