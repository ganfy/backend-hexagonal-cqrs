from unittest.mock import AsyncMock

import pytest

from src.contexts.auth.application.login_use_case import LoginUseCase
from src.contexts.auth.domain.login import Login
from src.contexts.users.domain.user import User
from src.core.exceptions.custom_exceptions import InvalidCredentialsException


@pytest.mark.asyncio
async def test_login_successful_with_valid_credentials():
    """
    Test successful login with valid credentials.
    """
    command = Login(email="test@example.com", password="correct_password")

    # Create a mock user found in the DB
    mock_user = AsyncMock(spec=User)
    mock_user.name = "Test User"
    # Mock `verify_password` to return True
    mock_user.verify_password.return_value = True

    # Create the user repository mock
    mock_user_repository = AsyncMock()
    mock_user_repository.find_by_email.return_value = mock_user

    # Instantiate the use case
    use_case = LoginUseCase(user_repository=mock_user_repository)

    # Act
    auth_token = await use_case.execute(command)

    # Assert
    # Verify user lookup by email
    mock_user_repository.find_by_email.assert_called_once_with(command.email)

    # Verify password verification call
    mock_user.verify_password.assert_called_once_with(command.password)

    # Check the returned token
    assert auth_token is not None
    assert auth_token.token_type == "bearer"
    assert "dummy-jwt-for-Test User" in auth_token.access_token


@pytest.mark.asyncio
async def test_login_fails_with_invalid_password():
    """
    Test login failure with invalid password.
    """
    command = Login(email="test@example.com", password="wrong_password")

    # Create a mock user
    mock_user = AsyncMock(spec=User)
    # Mock `verify_password` to return False
    mock_user.verify_password.return_value = False

    # Create the repository mock
    mock_user_repository = AsyncMock()
    mock_user_repository.find_by_email.return_value = mock_user

    use_case = LoginUseCase(user_repository=mock_user_repository)

    # Act & Assert
    with pytest.raises(InvalidCredentialsException):
        await use_case.execute(command)

    # Verify interactions
    mock_user_repository.find_by_email.assert_called_once_with(command.email)
    mock_user.verify_password.assert_called_once_with(command.password)


@pytest.mark.asyncio
async def test_login_fails_if_user_does_not_exist():
    """
    Test login failure if the email does not match any user.
    """
    command = Login(email="non.existent@example.com", password="any_password")

    # Create the repository mock
    mock_user_repository = AsyncMock()
    # Mock `find_by_email` to return None
    mock_user_repository.find_by_email.return_value = None

    use_case = LoginUseCase(user_repository=mock_user_repository)

    # Act & Assert
    with pytest.raises(InvalidCredentialsException):
        await use_case.execute(command)

    # Verify user lookup attempt
    mock_user_repository.find_by_email.assert_called_once_with(command.email)
