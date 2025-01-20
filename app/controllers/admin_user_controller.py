from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app.models.admin_user import AdminUser
from app.schemas.admin_user import AdminUserCreate, AdminUserUpdate
from fastapi import HTTPException, Request


# ฟังก์ชันในการสร้าง AdminUser ใหม่
def create_admin_user(db: Session, admin_user_create: AdminUserCreate) -> AdminUserInResponse:
    # ตรวจสอบว่า username ซ้ำหรือไม่
    existing_user = db.query(AdminUser).filter(AdminUser.username == admin_user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # สร้าง instance ของ AdminUser จากข้อมูลที่ได้รับ
    admin_user = AdminUser(
        username=admin_user_create.username,
        password=admin_user_create.password,  # อาจจะต้องมีการแฮชรหัสผ่านก่อนบันทึก
    )

    # เพิ่มข้อมูลลงในฐานข้อมูล
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)  # โหลดข้อมูลที่เพิ่งเพิ่มเข้ามาใหม่เพื่อให้ได้ค่า id, timestamps

    return AdminUserInResponse.from_orm(admin_user)