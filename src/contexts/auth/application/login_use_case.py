from src.contexts.auth.domain.auth_token import AuthToken
from src.contexts.auth.domain.login import Login
from src.contexts.users.application.user_repository import UserRepository
from src.core.exceptions.custom_exceptions import InvalidCredentialsException


class LoginUseCase:
    def __init__(self, user_repository: UserRepository):
        # We depend on the user repository to obtain user data
        self._user_repository = user_repository

    async def execute(self, command: Login) -> AuthToken:
        # Search for the user by their email
        user = await self._user_repository.find_by_email(command.email)

        # Verify if the user exists and if the password is correct
        if not user or not user.verify_password(command.password):
            raise InvalidCredentialsException("Invalid email or password.")

        # (Simulated) Create an access token
        # In a real application, a JWT would be generated here.
        dummy_token = f"dummy-jwt-for-{user.name}"

        return AuthToken(access_token=dummy_token, token_type="bearer")
