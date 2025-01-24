from datetime import datetime 
from sqlalchemy.orm import Session , joinedload 
from sqlalchemy import or_, asc, desc
from app.models.working import Working
from app.models.working_images import WorkingImages
from app.schemas.working import WorkingCreate, WorkingUpdate , WorkingResponse
from app.schemas.working_images import WorkingImageCreate, WorkingImageUpdate , WorkingImageResponse
from fastapi import HTTPException,Request 


def create_working_and_images(db: Session, working_create: WorkingCreate, working_image_create_list: list[WorkingImageCreate]) -> WorkingResponse:
    # สร้าง instance ของ Working จากข้อมูลที่ได้รับ
    working = Working(
        working_name=working_create.working_name,
        detail=working_create.detail,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # เพิ่มข้อมูล Working ลงในฐานข้อมูล
    db.add(working)
    db.commit()
    db.refresh(working)  # โหลดข้อมูลที่เพิ่งเพิ่มเข้ามาใหม่เพื่อให้ได้ค่า id, timestamps

    # สร้าง WorkingImages และเชื่อมโยงกับ Working ที่สร้างขึ้น
    working_images = []
    for image_create in working_image_create_list:
        working_image = WorkingImages(
            working_id=working.id,  # เชื่อมโยงกับ Working
            working_image_data=image_create.working_image_data,  # เก็บ Base64 ของรูปภาพ
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        working_images.append(working_image)

    # เพิ่มข้อมูล WorkingImages ลงในฐานข้อมูล
    db.add_all(working_images)
    db.commit()

    # คืนค่าผลลัพธ์
    return WorkingResponse.from_orm(working)



def update_working_and_images(
    db: Session, 
    working_id: int, 
    working_update: WorkingUpdate, 
    working_image_update_list: list[WorkingImageUpdate]
) -> WorkingResponse:
    # ค้นหาข้อมูล Working ที่ต้องการอัปเดต
    working = db.query(Working).filter(Working.id == working_id).first()
    if not working:
        raise HTTPException(status_code=404, detail="Working not found")

    # อัปเดตข้อมูล Working
    working.working_name = working_update.working_name or working.working_name
    working.detail = working_update.detail or working.detail
    working.updated_at = datetime.now()

    db.commit()
    db.refresh(working)

    # อัปเดตข้อมูล WorkingImages
    for image_update in working_image_update_list:
        working_image = db.query(WorkingImages).filter(
            WorkingImages.working_id == working_id,
            WorkingImages.id == image_update.id
        ).first()

        if not working_image:
            raise HTTPException(status_code=404, detail="Working Image not found")

        # อัปเดตข้อมูลรูปภาพ
        working_image.working_image_data = image_update.working_image_data or working_image.working_image_data
        working_image.updated_at = datetime.utcnow()

    db.commit()

    # คืนค่าผลลัพธ์
    return WorkingResponse.from_orm(working)


def get_working_by_id(db: Session, working_id: int) -> WorkingResponse:
    working = db.query(Working).filter(Working.id == working_id, Working.deleted_at == None).first()

    if not working:
        raise HTTPException(status_code=404, detail="Working not found")

    # ค้นหาภาพที่เกี่ยวข้องกับ working_id นี้
    working_images = db.query(WorkingImages).filter(WorkingImages.working_id == working_id, WorkingImages.deleted_at == None).all()

    # แปลงข้อมูล working และ working_images ให้เป็น response ที่ต้องการ
    working_response = WorkingResponse.from_orm(working)
    
    # แปลงข้อมูล working_images เป็น list ของ WorkingImageResponse
    working_response.images = [WorkingImageResponse.from_orm(image) for image in working_images]

    return working_response 



def get_all_working(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> dict:
    # Query สำหรับค้นหา Working
    query = db.query(Working).filter(Working.deleted_at.is_(None))

    # คำนวณจำนวนข้อมูลทั้งหมดในฐานข้อมูล
    total = query.count()

    # ค้นหา Working พร้อมจัดการ Pagination
    workings = query.offset(skip).limit(limit).all()

    # คำนวณจำนวนหน้า (total pages)
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    # คำนวณหมายเลขหน้าปัจจุบัน
    current_page = (skip // limit) + 1

    # คำนวณ next และ prev page
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    # สร้าง next_page_url และ prev_page_url
    next_page_url = (
        f"api/workings/?skip={(next_page - 1) * limit}&limit={limit}" if next_page else None
    )
    prev_page_url = (
        f"api/workings/?skip={(prev_page - 1) * limit}&limit={limit}" if prev_page else None
    )

    # ตรวจสอบว่ามีข้อมูลหรือไม่
    if not workings:
        raise HTTPException(status_code=404, detail="No work items found")

    # สร้าง response list สำหรับทุก working
    working_responses = []
    for working in workings:
        # ดึงข้อมูล working_images ที่เกี่ยวข้องกับ working.id
        working_images = db.query(WorkingImages).filter(
            WorkingImages.working_id == working.id,
            WorkingImages.deleted_at.is_(None)
        ).all()

        # แปลงข้อมูล working เป็น WorkingResponse
        working_response = WorkingResponse.from_orm(working)

        # แปลงข้อมูล working_images เป็น list ของ WorkingImageResponse
        working_response.images = [WorkingImageResponse.from_orm(image) for image in working_images]

        # เพิ่ม response ที่แปลงแล้วลงใน list
        working_responses.append(working_response)

    # สร้าง response object
    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": current_page,
        "next_page_url": next_page_url,
        "prev_page_url": prev_page_url,
        "workings": working_responses,
    }


def soft_delete_working(db: Session, working_id: int):
    # ค้นหา Working ที่ต้องการลบ
    working = db.query(Working).filter(Working.id == working_id).first()

    if not working:
        raise HTTPException(status_code=404, detail="Working not found")

    if working.deleted_at:
        raise HTTPException(status_code=400, detail="Working already deleted")

    # อัปเดต deleted_at ของ Working
    working.deleted_at = datetime.now()

    # ค้นหา WorkingImages ที่เกี่ยวข้องกับ Working นี้
    working_images = db.query(WorkingImages).filter(WorkingImages.working_id == working_id).all()

    # อัปเดต deleted_at ของ WorkingImages
    for image in working_images:
        if not image.deleted_at:  # ตรวจสอบว่าภาพยังไม่ถูกลบ
            image.deleted_at = datetime.now()

    # บันทึกการเปลี่ยนแปลง
    db.commit()
    db.refresh(working)








