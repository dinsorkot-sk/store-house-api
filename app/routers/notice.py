from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeInResponse , NoticeResponse
from app.database import SessionLocal
from app.controllers.notice_controller import (
    create_notice,
    update_notice,
    get_notice,
    get_notices,
    delete_notice
)

def get_session_local():
    yield SessionLocal()

router = APIRouter(
    prefix="/api/notices",
    tags=["notices"],
)

# สร้าง Notice ใหม่
@router.post("/", response_model=NoticeInResponse)
def add_notice(notice_create: NoticeCreate, db: Session = Depends(get_session_local)):
    return create_notice(db=db, notice_create=notice_create)

# ดึงข้อมูล Notice ทั้งหมด
@router.get("/", response_model=NoticeResponse)
def read_notices(
    skip: int = 0,
    limit: int = 10,
    keyword: str | None = None,
    order_price: str | None = None,
    order_size: str | None = None,
    order_notices: str | None = None,
    db: Session = Depends(get_session_local),
):
    return get_notices(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        order_price=order_price,
        order_size=order_size,
        order_notices=order_notices,
    )

# ดึงข้อมูล Notice ตาม ID
@router.get("/{notice_id}", response_model=NoticeInResponse)
def read_notice(notice_id: int, db: Session = Depends(get_session_local)):
    return get_notice(db=db, notice_id=notice_id)

# อัปเดตข้อมูล Notice
@router.put("/{notice_id}", response_model=NoticeInResponse)
def modify_notice(
    notice_id: int,
    notice_update: NoticeUpdate,
    db: Session = Depends(get_session_local),
):
    return update_notice(db=db, notice_id=notice_id, notice_update=notice_update)

# ลบข้อมูล Notice ตาม ID
@router.delete("/{notice_id}", response_model=NoticeInResponse)
def drop_notice(notice_id: int, db: Session = Depends(get_session_local)):
    return delete_notice(db=db, notice_id=notice_id)
