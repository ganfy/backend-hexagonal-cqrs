import uuid
from dataclasses import asdict
from typing import Optional

from src.contexts.users.application.user_query_repository import UserQueryRepository
from src.contexts.users.domain.read_user import ReadUser
from src.core.exceptions.custom_exceptions import UserNotFoundException


class GetUserUseCase:
    def __init__(self, user_query_repository: UserQueryRepository):
        self._user_query_repository = user_query_repository

    async def execute(self, user_id: uuid.UUID) -> Optional[ReadUser]:
        user = await self._user_query_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found.")

        user_dict = asdict(user)
        return ReadUser.model_validate(user_dict)
