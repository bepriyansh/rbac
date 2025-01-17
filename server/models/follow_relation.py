from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class FollowRelation(BaseModel):
    id: Optional[str]  # MongoDB will generate this
    follower_id: str  # User who is following
    followed_id: str  # User who is being followed
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        orm_mode = True
