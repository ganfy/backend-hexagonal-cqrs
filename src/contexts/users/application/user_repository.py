from abc import ABC, abstractmethod
from typing import Optional

from src.contexts.users.domain.user import User


class UserRepository(ABC):
    """
    Port for user repository operations.
    Defines the contract that architecture adapters must implement.
    """

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError
