from pydantic import BaseModel, EmailStr
from datetime import datetime

# What we ACCEPT when registering
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# What we SEND BACK (never send password back!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows reading from DB model

# What we ACCEPT when logging in
class UserLogin(BaseModel):
    email: str
    password: str

# Token response schema (NEW!)
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data schema (NEW!)
class TokenData(BaseModel):
    user_id: int