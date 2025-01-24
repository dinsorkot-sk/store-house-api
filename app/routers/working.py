from fastapi import APIRouter, Depends, Request , HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.working import WorkingCreate , WorkingResponse , WorkingUpdate
from app.schemas.working_images import WorkingImageCreate , WorkingImageUpdate
from app.controllers.working_controller import create_working_and_images , update_working_and_images , get_working_by_id , get_all_working ,soft_delete_working

def get_session_local():
    yield SessionLocal()

router = APIRouter(
    prefix="/api",
    tags=["api working"],
)

@router.post("/working/", response_model=WorkingResponse)
def add_working_and_images(
    working_create: WorkingCreate,
    working_image_create_list: list[WorkingImageCreate],
    db: Session = Depends(get_session_local)
):
    return create_working_and_images(db=db, working_create=working_create, working_image_create_list=working_image_create_list)


@router.put("/working/{working_id}", response_model=WorkingResponse)
def update_working_and_images_route(
    working_id: int,
    working_update: WorkingUpdate,
    working_image_update_list: list[WorkingImageUpdate],
    db: Session = Depends(get_session_local)
):
    return update_working_and_images(
        db=db,
        working_id=working_id,
        working_update=working_update,
        working_image_update_list=working_image_update_list
    )

@router.get("/working/{working_id}", response_model=WorkingResponse)
def get_working_route(working_id: int, db: Session = Depends(get_session_local)):
    return get_working_by_id(db=db, working_id=working_id)


@router.get("/working", response_model=dict)
def get_all_workings_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_session_local)):
    return get_all_working(db=db, skip=skip, limit=limit)


@router.delete("/working/{working_id}")
def delete_working(working_id: int, db: Session = Depends(get_session_local)):
    soft_delete_working(db=db, working_id=working_id)
    return {"detail": "Working and related images soft deleted successfully"}



