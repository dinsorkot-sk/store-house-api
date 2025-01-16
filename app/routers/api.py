
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeInResponse
from app.database import SessionLocal
from app.controllers.notice_controller import create_notice, update_notice, get_notice , get_notices

def get_session_local():
    yield SessionLocal()

router = APIRouter(prefix="/api",tags=["api"],)

# ดึงข้อมูล Notice ทั้งหมด
@router.get("/notices/")
async def read_notices(skip: int = 0, limit: int = 10, request: Request = None , db: Session = Depends(get_session_local)):
    # เรียกใช้ฟังก์ชัน get_notices เพื่อดึงข้อมูลพร้อมกับ pagination
    return get_notices(db=db, skip=skip, limit=limit , request=request)

# สร้าง Notice ใหม่
@router.post("/notices/", response_model=NoticeInResponse)
def add_notice(notice_create: NoticeCreate, db: Session = Depends(get_session_local)):
    return create_notice(db=db, notice_create=notice_create)

# อัปเดตข้อมูล Notice
@router.put("/notices/{notice_id}", response_model=NoticeInResponse)
def modify_notice(notice_id: int, notice_update: NoticeUpdate, db: Session = Depends(get_session_local)):
    return update_notice(db=db, notice_id=notice_id, notice_update=notice_update)

# ดึงข้อมูล Notice ตาม ID
@router.get("/notices/{notice_id}", response_model=NoticeInResponse)
def read_notice(notice_id: int, db: Session = Depends(get_session_local)):
    return get_notice(db=db, notice_id=notice_id)