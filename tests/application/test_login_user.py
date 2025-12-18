import pytest
from unittest.mock import MagicMock
from src.application.use_cases.login_user import LoginUserUseCase
from src.domain.user import User

@pytest.fixture
def mock_user_repo():
    repo = MagicMock()
    # A hashed version of 'password123'
    hashed_pass = "$2b$12$EixZaYVK12.S6.3a.i9v.O3.3a.i9v.O3.3a.i9v.O3.3a.i"
    user = User(id=1, username="testuser", email="test@example.com", hashed_password=hashed_pass)
    repo.get_by_email.return_value = user
    return repo

def test_login_user_success(mock_user_repo, mocker):
    # Arrange
    mocker.patch('passlib.context.CryptContext.verify', return_value=True)
    mocker.patch('jwt.encode', return_value="fake_token")
    login_use_case = LoginUserUseCase(mock_user_repo)

    # Act
    token = login_use_case.execute("test@example.com", "password123")

    # Assert
    mock_user_repo.get_by_email.assert_called_with("test@example.com")
    assert token == "fake_token"

def test_login_user_invalid_password(mock_user_repo, mocker):
    # Arrange
    mocker.patch('passlib.context.CryptContext.verify', return_value=False)
    login_use_case = LoginUserUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email or password"):
        login_use_case.execute("test@example.com", "wrongpassword")

def test_login_user_not_found(mock_user_repo):
    # Arrange
    mock_user_repo.get_by_email.return_value = None
    login_use_case = LoginUserUseCase(mock_user_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email or password"):
        login_use_case.execute("nonexistent@example.com", "password123")
