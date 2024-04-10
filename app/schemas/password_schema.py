from pydantic import BaseModel
from typing import List, Optional


class PasswordBase(BaseModel):
    nombre: str


class PasswordCreate(PasswordBase):
    pass


class Password(PasswordBase):
    id: int

    class Config:
        from_attributes = True
