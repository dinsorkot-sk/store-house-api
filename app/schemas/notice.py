# schemas/notice.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None
    location: str
    size: Optional[str] = None
    office_size: Optional[str] = None
    details: Optional[str] = None
    preferred_contact_phone: Optional[bool] = False
    preferred_contact_email: Optional[bool] = False
    poster_type: Optional[str] = None
    price: Optional[float] = None

class NoticeCreate(BaseModel):
    title: str
    first_name: str
    last_name: str
    phone: str
    email: str
    location: str
    size: str
    office_size: str
    details: str
    preferred_contact_phone: bool
    preferred_contact_email: bool
    poster_type: str
    price: float

class NoticeUpdate(NoticeBase):
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    size: Optional[str] = None
    office_size: Optional[str] = None
    details: Optional[str] = None
    preferred_contact_phone: Optional[bool] = None
    preferred_contact_email: Optional[bool] = None
    poster_type: Optional[str] = None
    price: Optional[float] = None

class NoticeInResponse(NoticeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # ช่วยให้ Pydantic ใช้ข้อมูลจาก SQLAlchemy model ได้
