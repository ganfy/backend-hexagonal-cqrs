import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class ReadUser(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
