from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.contexts.users.application.user_repository import UserRepository
from src.contexts.users.domain.user import User
from src.contexts.users.infrastructure.user import User as UserOrmModel
from src.contexts.users.infrastructure.user_mappers import (
    user_domain_to_orm,
    user_orm_to_domain,
)


class UserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        orm_user = user_domain_to_orm(user)
        self._session.add(orm_user)
        await self._session.flush()

    async def find_by_email(self, email: str) -> Optional[User]:
        query = select(UserOrmModel).filter(UserOrmModel.email == email)
        result = await self._session.execute(query)
        orm_user = result.scalars().first()
        if orm_user:
            return user_orm_to_domain(orm_user)
        return None
