from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.contexts.auth.application.login_use_case import LoginUseCase
from src.contexts.users.infrastructure.user_repository import UserRepository
from src.core.database.database import get_db


def get_login_use_case(session: AsyncSession = Depends(get_db)) -> LoginUseCase:
    user_repository = UserRepository(session)
    return LoginUseCase(user_repository=user_repository)
