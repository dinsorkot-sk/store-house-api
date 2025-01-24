from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.inquirer import InquirerCreate, InquirerUpdate, InquirerResponse
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
    prefix="/api",
    tags=["api inquirers"],
)


# สร้าง Inquirers ใหม่
@router.post("/inquirers/", response_model=InquirerResponse)
def add_inquirer(inquirer: InquirerCreate, db: Session = Depends(get_session_local)):
    return create_inquirer(db=db, inquirer=inquirer)


#  ดึงข้อมูล Inquirers ทั้งหมด
@router.get("/inquirers/", response_model=InquirerResponse)
def read_inquirers(
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_inquirers: str = None,
    request: Request = None,
    db: Session = Depends(get_session_local),
):
    return get_inquirers(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        order_inquirers=order_inquirers,
        request=request,
    )


#  ดึงข้อมูล Inquirers ตาม ID
@router.get("/inquirers/{inquirer_id}", response_model=InquirerResponse)
def read_inquirer(inquirer_id: int, db: Session = Depends(get_session_local)):
    return get_inquirer(db=db, inquirer_id=inquirer_id)


# อัพเดท Inquirers ตาม ID
@router.put("/inquirers/{inquirer_id}", response_model=InquirerResponse)
def update_inquirer(
    inquirer_id: int, inquirer: InquirerUpdate, db: Session = Depends(get_session_local)
):
    return update_inquirer(db=db, inquirer_id=inquirer_id, inquirer_update=inquirer)


# ลบ Inquirers ตาม ID
@router.delete("/inquirers/{inquirer_id}", response_model=InquirerResponse)
def drop_inquirer(inquirer_id: int, db: Session = Depends(get_session_local)):
    return delete_inquirer(db=db, inquirer_id=inquirer_id)
