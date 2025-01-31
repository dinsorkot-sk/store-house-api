from fastapi import APIRouter, Depends, Request , HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.admin_user import AdminUserCreate , AdminUserResponse , AdminUserUpdate
from app.controllers.admin_user_controller import create_admin_user , update_admin_user , soft_delete_admin_user , login_admin_user

def get_session_local():
    yield SessionLocal()


router = APIRouter(
    prefix="/api",
    tags=["api admin_user (ผู้ดูแลระบบ)"],
)

@router.post(
    "/admin_user/",
    response_model=AdminUserResponse,
    summary="เพิ่มผู้ดูแลระบบ",
    description="ใช้สำหรับเพิ่มข้อมูลผู้ดูแลระบบใหม่",
)
def add_adminuser(admin_user_create: AdminUserCreate, db: Session = Depends(get_session_local)):
    return create_admin_user(db=db, admin_user_create=admin_user_create)


@router.put(
    "/admin_user/{admin_user_id}",
    response_model=AdminUserResponse,
    summary="แก้ไขข้อมูลผู้ดูแลระบบ",
    description="ใช้สำหรับแก้ไขข้อมูลผู้ดูแลระบบตาม ID ที่ระบุ",
)
def modify_adminuser(
    admin_user_id: int,
    admin_user_update: AdminUserUpdate,
    db: Session = Depends(get_session_local),
):
    return update_admin_user(db=db, admin_user_id=admin_user_id, admin_user_update=admin_user_update)


@router.delete(
    "/admin_user/{admin_user_id}",
    response_model=AdminUserResponse,
    summary="ลบข้อมูลผู้ดูแลระบบ",
    description="ใช้สำหรับลบข้อมูลผู้ดูแลระบบตาม ID ที่ระบุ",
)
def drop_admin_user(admin_user_id: int, db: Session = Depends(get_session_local)):
    return soft_delete_admin_user(db=db, admin_user_id=admin_user_id)


@router.post(
    "/admin_user/login/",
    summary="เข้าสู่ระบบผู้ดูแล",
    description="ใช้สำหรับเข้าสู่ระบบของผู้ดูแลระบบโดยต้องระบุ username และ password",
)
def login_adminuser(username: str, password: str, request: Request, db: Session = Depends(get_session_local)):
    try:
        user_data = login_admin_user(db=db, username=username, password=password)
        request.state.user = user_data
        return user_data
    except HTTPException as e:
        raise e





