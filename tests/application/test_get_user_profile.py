import pytest
from unittest.mock import MagicMock
from src.application.use_cases.get_user_profile import GetUserProfileUseCase
from src.domain.user import User

def test_get_user_profile_success():
    # Arrange
    mock_user_repo = MagicMock()
    user = User(id=1, username="testuser", email="test@example.com", hashed_password="hashed")
    mock_user_repo.get_by_id.return_value = user

    get_profile_case = GetUserProfileUseCase(mock_user_repo)

    # Act
    result = get_profile_case.execute(user_id=1)

    # Assert
    mock_user_repo.get_by_id.assert_called_with(1)
    assert result == user

def test_get_user_profile_not_found():
    # Arrange
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id.return_value = None

    get_profile_case = GetUserProfileUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found"):
        get_profile_case.execute(user_id=999)
