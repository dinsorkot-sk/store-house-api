from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.working_images import WorkingImageResponse


class WorkingBase(BaseModel):
    working_name: Optional[str] = None
    detail: Optional[str] = None
    create_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deated_at: Optional[datetime] = None
   

class WorkingCreate(BaseModel):
    working_name: str
    detail: str
    create_at: datetime

class WorkingUpdate(WorkingBase):
    working_name: Optional[str] = None
    detail: Optional[str] = None
    updated_at: Optional[datetime] = None

class WorkingResponse(WorkingBase):
    id : int
    create_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deated_at: Optional[datetime] = None
    images: List[WorkingImageResponse] = []
    class Config:
        from_attributes = True


class WorkingListResponse(BaseModel):
    total: int
    total_pages: int
    current_page: int
    next_page_url: Optional[str]
    prev_page_url: Optional[str]
    workings: List[WorkingResponse]