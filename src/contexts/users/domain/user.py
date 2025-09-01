import uuid
from dataclasses import dataclass, field

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:
    name: str
    email: str
    hashed_password: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a plaintext password."""
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifies a plaintext password against the stored hashed password."""
        return pwd_context.verify(password, self.hashed_password)
