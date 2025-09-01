from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.contexts.users.application.get_user_use_case import GetUserUseCase
from src.contexts.users.infrastructure.user_repository import UserRepository
from src.core.database.database import get_db


def get_user_query_use_case(session: AsyncSession = Depends(get_db)) -> GetUserUseCase:
    repository = UserRepository(session)
    return GetUserUseCase(repository)
