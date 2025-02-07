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

class ContactInResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ContactResponse(BaseModel):
    total: int
    total_pages: int
    current_page: int
    next_page_url: Optional[str] = None
    prev_page_url: Optional[str] = None
    contacts: list[ContactInResponse]