from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime, timezone

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class User(BaseModel):
    id: Optional[str]  # MongoDB will generate this
    name: str
    email: str
    password: str  # Password will be hashed
    age: int
    gender: Optional[Gender]
    role: UserRole = UserRole.user  # Default to 'user'
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
