from pydantic import BaseModel
from datetime import datetime

# What we ACCEPT when creating a post
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True  # default is published

# What we ACCEPT when updating
class PostUpdate(BaseModel):
    title: str = None
    content: str = None
    published: bool = None

# What we SEND BACK
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True