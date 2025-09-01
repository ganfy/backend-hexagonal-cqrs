import uuid
from abc import ABC, abstractmethod
from typing import Optional

from src.contexts.users.domain.read_user import ReadUser


class UserQueryRepository(ABC):
    """
    Puerto para las operaciones de consulta de usuarios.
    """

    @abstractmethod
    async def find_by_id(self, user_id: uuid.UUID) -> Optional[ReadUser]:
        raise NotImplementedError
