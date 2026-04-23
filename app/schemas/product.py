from pydantic import BaseModel
from datetime import datetime

# What we ACCEPT when creating
class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    stock: int = 0

# What we ACCEPT when updating
class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    stock: int = None

# What we SEND BACK
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    stock: int
    created_at: datetime

    class Config:
        from_attributes = True