from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.inquirer import InquirerCreate, InquirerUpdate, InquirerResponse , InquirerInResponse
from app.database import SessionLocal
from app.controllers.inquirer_controller import (
    create_inquirer,
    get_inquirer,
    get_inquirers,
    update_inquirer,
    delete_inquirer,
)


def get_session_local():
    yield SessionLocal()


router = APIRouter(
    prefix="/api/inquirer",
    tags=["api inquirers (ผู้สอบถาม)"],
)


# ดึงรายการ Inquirers ทั้งหมด
@router.get(
    "/",
    response_model=InquirerResponse,
    summary="ดึงรายการ Inquirers ทั้งหมด",
    description="""
    ใช้สำหรับดึงรายการ Inquirers ทั้งหมด สามารถเพิ่มตัวกรองและการเรียงลำดับได้  
    - **skip**: จำนวนรายการที่ข้าม (default = 0)  
    - **limit**: จำนวนรายการที่ต้องการดึง (default = 10)  
    - **keyword**: คำค้นหาที่ใช้สำหรับค้นหาในชื่อหรือรายละเอียด  
    - **order_inquirers**: เรียงลำดับตามเวลาที่สร้าง (`asc` หรือ `desc`)  
    """,
)
def read_inquirers(
    skip: int = 0,
    limit: int = 10,
    keyword: str | None = None,
    order_inquirers: str = 'asc',
    db: Session = Depends(get_session_local),
):
    return get_inquirers(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        order_inquirers=order_inquirers,
    )


# สร้าง Inquirer ใหม่
@router.post(
    "/",
    response_model=InquirerInResponse,
    summary="สร้าง Inquirer ใหม่",
    description="ใช้สำหรับเพิ่มข้อมูล Inquirer ลงในระบบ",
)
def add_inquirer(inquirer: InquirerCreate, db: Session = Depends(get_session_local)):
    return create_inquirer(db=db, inquirer=inquirer)


# ดึงข้อมูล Inquirer ตาม ID
@router.get(
    "/{inquirer_id}",
    response_model=InquirerInResponse,
    summary="ดึงข้อมูล Inquirer ตาม ID",
    description="ใช้สำหรับดึงข้อมูล Inquirer รายบุคคลตาม ID ที่ระบุ",
)
def read_inquirer(inquirer_id: int, db: Session = Depends(get_session_local)):
    return get_inquirer(db=db, inquirer_id=inquirer_id)




@router.put(
    "/{inquirer_id}",
    response_model=InquirerInResponse,  # Use InquirerInResponse to match the return type
    summary="อัปเดตข้อมูล Inquirer",
    description="ใช้สำหรับอัปเดตข้อมูล Inquirer ตาม ID ที่ระบุ",
)
def update_inquirer_route(
    inquirer_id: int, inquirer: InquirerUpdate, db: Session = Depends(get_session_local)
):
    # Call the service function to handle the update
    return update_inquirer(db=db, inquirer_id=inquirer_id, inquirer_update=inquirer)


# ลบ Inquirer ตาม ID
@router.delete(
    "/{inquirer_id}",
    response_model=InquirerInResponse,  # Use InquirerInResponse to match the return type
    summary="ลบข้อมูล Inquirer",
    description="ใช้สำหรับลบข้อมูล Inquirer ตาม ID ที่ระบุ",
)
def drop_inquirer(inquirer_id: int, db: Session = Depends(get_session_local)):
    # Call the service function to handle the soft delete
    return delete_inquirer(db=db, inquirer_id=inquirer_id)