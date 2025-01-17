from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId

class Comment(BaseModel):
    id: Optional[str]
    post_id: str
    user_id: str
    content: str
    parent_comment_id: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
    likes: List[str] = []  # List of user IDs who liked the comment
    reply_count: int = 0  
    
    class Config:
        orm_mode = True

class CommentInResponse(BaseModel):
    id: str
    post_id: str
    user_id: str
    content: str
    created_at: datetime
    parent_comment_id: Optional[str]
    likes_count: int  
    reply_count: int  
    
    class Config:
        orm_mode = True
