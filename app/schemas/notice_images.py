from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticeImageBase(BaseModel):
    # notice_id: int
    image_path: str


class NoticeImageCreate(NoticeImageBase):
    pass


class NoticeImageUpdate(BaseModel):
    image_path: Optional[str]  # Only allow updating the `image_path`


class NoticeImageResponse(NoticeImageBase):
    id: int
    created_at: datetime
    uploaded_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models
