from pydantic import BaseModel
from datetime import datetime

# What we ACCEPT when creating a todo
class TodoCreate(BaseModel):
    title: str
    description: str = None  # optional field

# What we ACCEPT when updating a todo
class TodoUpdate(BaseModel):
    title: str = None        # all fields optional for update
    description: str = None
    completed: bool = None

# What we SEND BACK
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True