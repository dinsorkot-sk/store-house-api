from pydantic import BaseModel
from typing import Optional
from datetime import datetime 


class WorkingImageBase(BaseModel):
    working_id: int
    working_image_data : Optional[str] = None
    
class WorkingImageCreate(WorkingImageBase):
    working_image_data : str

class WorkingImageUpdate(WorkingImageBase):
    id : int
    working_id : Optional[int] = None
    working_image_data : Optional[str] = None
    update_at: Optional[datetime] = None

class WorkingImageResponse(WorkingImageBase):
    id : int
    working_id : int
    working_image_data : str
    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
    delete_at: Optional[datetime] = None
    class Config:
        from_attributes = True
        exclude = {"images"}
