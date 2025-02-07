from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.contacts import ContactCreate, ContactUpdate, ContactResponse , ContactInResponse
from app.database import SessionLocal
from app.controllers.contact_controller import (
    create_contact,
    update_contact,
    delete_contact,
    get_contact,
    get_contacts
)


def get_session_local():
    yield SessionLocal()


router = APIRouter(
    prefix="/api",
    tags=["api contacts"],
)


@router.post(
    "/contacts/",
    response_model=ContactInResponse,
    summary="เพิ่มข้อมูล Contact",
    description="ใช้สำหรับเพิ่มข้อมูล Contact ใหม่เข้าสู่ระบบ",
)
def add_contact(contact_create: ContactCreate, db: Session = Depends(get_session_local)):
    return create_contact(db=db, contact_create=contact_create)


@router.get(
    "/contacts/",
    response_model=ContactResponse,
    summary="ดึงข้อมูล Contacts ทั้งหมด",
    description="ใช้สำหรับดึงข้อมูล Contacts ทั้งหมดจากฐานข้อมูล สามารถกำหนดจำนวนข้อมูลที่ต้องการดึงและเรียงลำดับได้",
)
def read_contacts(
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_contacts: str = None,
    db: Session = Depends(get_session_local),
):
    return get_contacts(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        order_contacts=order_contacts,
    )


@router.get(
    "/contacts/{contact_id}",
    response_model=ContactInResponse,
    summary="ดึงข้อมูล Contact ตาม ID",
    description="ใช้สำหรับดึงข้อมูล Contact ตาม ID ที่ระบุ",
)
def read_contact(contact_id: int, db: Session = Depends(get_session_local)):
    return get_contact(db=db, contact_id=contact_id)


@router.put(
    "/contacts/{contact_id}",
    response_model=ContactInResponse,
    summary="อัปเดตข้อมูล Contact",
    description="ใช้สำหรับอัปเดตข้อมูล Contact ตาม ID ที่ระบุ",
)
def put_contact(
    contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_session_local)
):
    return update_contact(db=db, contact_id=contact_id, contact_update=contact_update)


@router.delete(
    "/contacts/{contact_id}",
    response_model=ContactInResponse,
    summary="ลบข้อมูล Contact",
    description="ใช้สำหรับลบข้อมูล Contact ตาม ID ที่ระบุ",
)
def drop_contact(contact_id: int, db: Session = Depends(get_session_local)):
    return delete_contact(db=db, contact_id=contact_id)