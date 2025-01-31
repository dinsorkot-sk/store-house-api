from pydantic import BaseModel
from typing import Optional
from datetime import datetime




class AdminUserBase(BaseModel):
    username : str
    password : str


class AdminUserCreate(BaseModel):
    username: str
    password: str

class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class AdminUserBase(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class AdminUserResponse(AdminUserBase):
    id : int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] 


    class Config:
        from_attributes = True