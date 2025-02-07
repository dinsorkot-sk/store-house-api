from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContactImageBase(BaseModel):
    # contact_id: int
    image_path: str

class ContactImageCreate(ContactImageBase):
    pass

class ContactImageUpdate(BaseModel):
    image_path: Optional[str] = None

class ContactImageResponse(ContactImageBase):
    id: int
    created_at: datetime
    uploaded_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
