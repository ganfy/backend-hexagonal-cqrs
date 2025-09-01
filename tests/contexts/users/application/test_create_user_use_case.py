from unittest.mock import AsyncMock, patch

import pytest

from src.contexts.users.application.create_user_use_case import CreateUserUseCase
from src.contexts.users.domain.create_user import CreateUser
from src.contexts.users.domain.user import User
from src.core.exceptions.custom_exceptions import UserAlreadyExistsException


@pytest.mark.asyncio
async def test_create_user_successfully():
    """
    Test successful user creation when the email does not already exist.
    """
    # Arrange
    command = CreateUser(
        name="New User", email="new.user@example.com", password="strong_password"
    )

    # Create a mock for the user repository
    mock_user_repository = AsyncMock()
    # Simulate that the user does NOT exist. `find_by_email` returns None.
    mock_user_repository.find_by_email.return_value = None

    # Instantiate the use case
    use_case = CreateUserUseCase(user_repository=mock_user_repository)

    # Act
    # Use patch to intercept the call to User.hash_password
    with patch.object(
        User, "hash_password", return_value="hashed_password_from_mock"
    ) as mock_hash:
        await use_case.execute(command)

    # Assert
    # Verify that we tried to find the user by email
    mock_user_repository.find_by_email.assert_called_once_with(command.email)

    # Verify that the hashing method was called with the correct password
    mock_hash.assert_called_once_with("strong_password")

    # Verify that the `save` method was called once
    mock_user_repository.save.assert_called_once()
    # Get the User object passed to `save`
    saved_user_arg = mock_user_repository.save.call_args[0][0]

    # Verify that the saved user has the correct data
    assert isinstance(saved_user_arg, User)
    assert saved_user_arg.name == command.name
    assert saved_user_arg.email == command.email
    assert saved_user_arg.hashed_password == "hashed_password_from_mock"


@pytest.mark.asyncio
async def test_create_user_fails_if_email_already_exists():
    """
    Test that an exception is raised if trying to create a user with an existing email.
    """
    # Arrange
    command = CreateUser(
        name="Existing User", email="existing.user@example.com", password="any_password"
    )

    # Create a mock for an existing user in the DB
    mock_existing_user = User(
        name="DB User", email="existing.user@example.com", hashed_password="some_hash"
    )

    # Create the mock repository
    mock_user_repository = AsyncMock()
    # Simulate that the user DOES exist. `find_by_email` returns the mocked user.
    mock_user_repository.find_by_email.return_value = mock_existing_user

    # Instantiate the use case
    use_case = CreateUserUseCase(user_repository=mock_user_repository)

    # Act & Assert
    # Verify that the correct exception is raised
    with pytest.raises(UserAlreadyExistsException) as excinfo:
        await use_case.execute(command)

    # Verify the exception message
    assert str(excinfo.value) == f"User with email {command.email} already exists."

    # Verify that we tried to find the user
    mock_user_repository.find_by_email.assert_called_once_with(command.email)

    # Verify that the `save` method was NEVER called
    mock_user_repository.save.assert_not_called()
