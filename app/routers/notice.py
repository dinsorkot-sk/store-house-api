from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeInResponse, NoticeResponse
from app.database import SessionLocal
from app.controllers.notice_controller import (
    create_notice,
    update_notice,
    get_notice,
    get_notices,
    delete_notice
)

def get_session_local():
    """Dependency ที่ใช้สำหรับดึง Session ของ Database"""
    yield SessionLocal()

router = APIRouter(
    prefix="/api/notices",
    tags=["notices (ประกาศเกี่ยวกับโกดัง)"],
)

# 🟢 สร้าง Notice ใหม่
@router.post(
    "/",
    response_model=NoticeInResponse,
    summary="สร้างประกาศใหม่",
    description="""
    ใช้สำหรับสร้างประกาศใหม่ในระบบ โดยต้องระบุข้อมูลของ Notice ผ่าน `NoticeCreate` schema  
    - **title**: ชื่อประกาศ  
    - **description**: รายละเอียดของประกาศ  
    - **price**: ราคาของประกาศ (ถ้ามี)  
    - **size**: ขนาดของรายการ (ถ้ามี)  
    """,
)
def add_notice(notice_create: NoticeCreate, db: Session = Depends(get_session_local)):
    return create_notice(db=db, notice_create=notice_create)

# 🔵 ดึงข้อมูล Notice ทั้งหมด
@router.get(
    "/",
    response_model=NoticeResponse,
    summary="ดึงรายการประกาศทั้งหมด",
    description="""
    ใช้สำหรับดึงรายการประกาศทั้งหมด สามารถเพิ่มตัวกรองและการเรียงลำดับได้  
    - **skip**: จำนวนรายการที่ข้าม (default = 0)  
    - **limit**: จำนวนรายการที่ต้องการดึง (default = 10)  
    - **keyword**: คำค้นหาที่ใช้สำหรับค้นหาใน title หรือ description  
    - **order_price**: เรียงลำดับตามราคา (`asc` หรือ `desc`)  
    - **order_size**: เรียงลำดับตามขนาด (`asc` หรือ `desc`)  
    - **order_notices**: เรียงลำดับตามเวลาที่สร้าง (`asc` หรือ `desc`)  
    """,
)
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

# 🔍 ดึงข้อมูล Notice ตาม ID
@router.get(
    "/{notice_id}",
    response_model=NoticeInResponse,
    summary="ดึงประกาศตาม ID",
    description="""
    ใช้สำหรับดึงข้อมูลประกาศเฉพาะ ID  
    - **notice_id**: ID ของประกาศที่ต้องการค้นหา  
    """,
)
def read_notice(notice_id: int, db: Session = Depends(get_session_local)):
    notice = get_notice(db=db, notice_id=notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="ไม่พบประกาศ")
    return notice

# 📝 อัปเดตข้อมูล Notice
@router.put(
    "/{notice_id}",
    response_model=NoticeInResponse,
    summary="แก้ไขประกาศ",
    description="""
    ใช้สำหรับอัปเดตข้อมูลของประกาศ โดยต้องระบุ ID ของประกาศที่ต้องการแก้ไข  
    - **notice_id**: ID ของประกาศที่ต้องการแก้ไข  
    - **title**: ชื่อประกาศใหม่ (ถ้ามี)  
    - **description**: รายละเอียดใหม่ (ถ้ามี)  
    - **price**: ราคาใหม่ (ถ้ามี)  
    - **size**: ขนาดใหม่ (ถ้ามี)  
    """,
)
def modify_notice(
    notice_id: int,
    notice_update: NoticeUpdate,
    db: Session = Depends(get_session_local),
):
    updated_notice = update_notice(db=db, notice_id=notice_id, notice_update=notice_update)
    if not updated_notice:
        raise HTTPException(status_code=404, detail="ไม่พบประกาศที่ต้องการแก้ไข")
    return updated_notice

# ❌ ลบข้อมูล Notice ตาม ID
@router.delete(
    "/{notice_id}",
    response_model=NoticeInResponse,
    summary="ลบประกาศ",
    description="""
    ใช้สำหรับลบประกาศจากระบบ โดยต้องระบุ ID ของประกาศที่ต้องการลบ  
    - **notice_id**: ID ของประกาศที่ต้องการลบ  
    """,
)
def drop_notice(notice_id: int, db: Session = Depends(get_session_local)):
    deleted_notice = delete_notice(db=db, notice_id=notice_id)
    if not deleted_notice:
        raise HTTPException(status_code=404, detail="ไม่พบประกาศที่ต้องการลบ")
    return deleted_notice
