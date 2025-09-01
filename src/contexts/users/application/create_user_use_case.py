from src.contexts.users.application.user_repository import UserRepository
from src.contexts.users.domain.create_user import CreateUser
from src.contexts.users.domain.user import User
from src.core.exceptions.custom_exceptions import UserAlreadyExistsException


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, command: CreateUser) -> None:
        # Verify if the user already exists
        existing_user = await self._user_repository.find_by_email(command.email)
        if existing_user:
            raise UserAlreadyExistsException(
                f"User with email {command.email} already exists."
            )

        # Hash the password
        hashed_password = User.hash_password(command.password)

        # Create domain user object
        new_user = User(
            name=command.name,
            email=command.email,
            hashed_password=hashed_password,
        )

        # Save the new user
        await self._user_repository.save(new_user)
