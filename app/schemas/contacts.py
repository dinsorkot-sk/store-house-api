from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.contact_images import ContactImageCreate

class ContactBase(BaseModel):
    order_number: int
    title: str
    url: str

class ContactCreate(ContactBase):
    images:list[ContactImageCreate]
    

class ContactUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    deleted_at: Optional[datetime] = None

class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    uploaded_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
