from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class Post(BaseModel):
    id: Optional[str]
    user_id: str 
    content: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None  
    likes_count: int = 0
    comments_count: int = 0

    class Config:
        orm_mode = True

class PostInResponse(BaseModel):
    id: str
    content: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    likes_count: int
    comments_count: int

    class Config:
        orm_mode = True
