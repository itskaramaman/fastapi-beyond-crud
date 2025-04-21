from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: UUID 
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: bool 
    created_at: datetime
    updated_at: datetime


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

