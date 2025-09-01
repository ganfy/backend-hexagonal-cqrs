import uuid

from pydantic import BaseModel, EmailStr


class ReadUser(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
