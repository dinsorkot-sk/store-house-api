from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
from app.models.inquirer import Inquirer
from app.schemas.inquirer import InquirerCreate, InquirerUpdate, InquirerInResponse , InquirerResponse
from fastapi import HTTPException, Request


def create_inquirer(db: Session, inquirer: InquirerCreate):
    inquirer = Inquirer(**inquirer.dict())
    db.add(inquirer)
    db.commit()
    db.refresh(inquirer)
    return InquirerInResponse.from_orm(inquirer)


def get_inquirer(db: Session, inquirer_id: int):
    inquirer = db.query(Inquirer).filter(Inquirer.id == inquirer_id, Inquirer.deleted_at == None).first()

    if not inquirer:
        raise HTTPException(status_code=404, detail="Inquirer not found")


    return InquirerInResponse.from_orm(inquirer)


def get_inquirers(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_inquirers: str = "desc",
    request: Request = None,
):
     # Query สำหรับค้นหา Inquirer
    query = db.query(Inquirer)
    
    # เพิ่มเงื่อนไขการค้นหา หากมี keyword
    if keyword:
        query = query.filter(
            or_(
                Inquirer.full_name.ilike(f"%{keyword}%"),
                Inquirer.email.ilike(f"%{keyword}%"),
                Inquirer.detail.ilike(f"%{keyword}%"),
                Inquirer.phone_number.ilike(f"%{keyword}%"),
            )
        )
        
     # จัดเรียงตามราคา (asc หรือ desc)
    if order_inquirers == "asc":
        query = query.order_by(asc(Inquirer.created_at))
    elif order_inquirers == "desc":
        query = query.order_by(desc(Inquirer.created_at))
    
    # ค้นหา Notice ทั้งหมดจากฐานข้อมูล
    inquirers = query.offset(skip).limit(limit).all()

    # คำนวณจำนวนข้อมูลทั้งหมดในฐานข้อมูล
    total = query.count()

    # คำนวณจำนวนหน้า (total pages)
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    # คำนวณหมายเลขหน้าปัจจุบัน
    current_page = (skip // limit) + 1

    # คำนวณ next และ prev page
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    # ตรวจสอบว่า request มีค่า prefix หรือไม่ และสร้าง URL
    base_url = str(request.base_url) if request else "http://localhost:8000/"
    # สร้าง next_page_url และ prev_page_url โดยใช้ url_for และค่าพารามิเตอร์ที่เหมาะสม
    next_page_url = (
        f"{base_url}api/notices/?skip={(next_page - 1) * limit}&limit={limit}"
        if next_page
        else None
    )
    prev_page_url = (
        f"{base_url}api/notices/?skip={(prev_page - 1) * limit}&limit={limit}"
        if prev_page
        else None
    )

    if not inquirers:
        raise HTTPException(status_code=404, detail="Inquirer not found")

    # สร้าง response ที่มีข้อมูลต่างๆ
    return InquirerResponse (
        total=total,
        total_pages=total_pages,
        current_page=current_page,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        inquirers=[InquirerInResponse.from_orm(inquirer) for inquirer in inquirers],
    )



def update_inquirer(db: Session, inquirer_id: int, inquirer_update: InquirerUpdate):
    inquirer = db.query(Inquirer).filter(Inquirer.id == inquirer_id).first()

    if inquirer is None:
        raise HTTPException(status_code=404, detail="Inquirer not found")

    # Update the fields based on the InquirerUpdate schema
    for key, value in inquirer_update.dict(exclude_unset=True).items():
        setattr(inquirer, key, value)
    
    # Commit the changes and refresh the instance
    db.commit()
    db.refresh(inquirer)

    # Return the updated inquirer as a response
    return InquirerInResponse.from_orm(inquirer)


def delete_inquirer(db: Session, inquirer_id: int):
    inquirer = db.query(Inquirer).filter(Inquirer.id == inquirer_id).first()

    if not inquirer:
        raise HTTPException(status_code=404, detail="Inquirer not found")

    # Perform soft delete
    inquirer.deleted_at = datetime.now()
    db.commit()
    db.refresh(inquirer)

    # Return the updated inquirer as a response
    return InquirerInResponse.from_orm(inquirer)
