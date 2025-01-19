from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InquirerCreate(BaseModel):
    notice_id: int
    full_name: str
    phone_number: str
    email: str
    detail: str

class InquirerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    detail: Optional[str] = None

class InquirerResponse(BaseModel):
    id: int
    notice_id: int
    full_name: str
    phone_number: str
    email: str
    detail: str
    created_at: datetime
    uploaded_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
