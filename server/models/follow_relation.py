from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class FollowRelation(BaseModel):
    id: Optional[str] 
    follower_id: str 
    followed_id: str  
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        orm_mode = True
