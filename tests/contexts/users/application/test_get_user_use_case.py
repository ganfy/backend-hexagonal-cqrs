import uuid
from unittest.mock import AsyncMock

import pytest

from src.contexts.users.application.get_user_use_case import GetUserUseCase
from src.contexts.users.domain.user import User
from src.core.exceptions.custom_exceptions import UserNotFoundException


@pytest.mark.asyncio
async def test_get_user_by_id_when_user_exists():
    """
    Test the use case for retrieving a user when they exist.
    Verify that the repository is called and a UserReadModel is returned.
    """
    user_id = uuid.uuid4()
    # Create a mock user entity
    mock_user = User(
        id=user_id,
        name="Test User",
        email="test@example.com",
        hashed_password="hashed_password_value",
    )

    # Create a mock query repository
    mock_query_repository = AsyncMock()
    # Configure the mock to return the mock user
    mock_query_repository.find_by_id.return_value = mock_user

    # Instantiate the use case with the mocked repository
    use_case = GetUserUseCase(user_query_repository=mock_query_repository)

    # Execute the use case
    user_read_model = await use_case.execute(user_id)

    # Verify the repository method was called once with the correct arguments
    mock_query_repository.find_by_id.assert_called_once_with(user_id)

    # Check that the result is not None and has the correct data
    assert user_read_model is not None
    assert user_read_model.id == user_id
    assert user_read_model.name == "Test User"
    assert user_read_model.email == "test@example.com"
    assert not hasattr(user_read_model, "hashed_password")


@pytest.mark.asyncio
async def test_get_user_by_id_raises_exception_when_user_not_found():
    """
    Test that a UserNotFoundException is raised when the user does not exist.
    """
    non_existent_id = uuid.uuid4()

    # Create a mock query repository
    mock_query_repository = AsyncMock()
    # Configure the mock to return None, simulating a user not found
    mock_query_repository.find_by_id.return_value = None

    # Instantiate the use case
    use_case = GetUserUseCase(user_query_repository=mock_query_repository)

    # Verify that the expected exception is raised
    with pytest.raises(UserNotFoundException) as excinfo:
        await use_case.execute(non_existent_id)

    # Check the exception message
    assert str(excinfo.value) == f"User with id {non_existent_id} not found."

    # Verify the repository was called correctly
    mock_query_repository.find_by_id.assert_called_once_with(non_existent_id)
