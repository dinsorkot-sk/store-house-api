from fastapi import FastAPI
from app.database import Base, engine
from app.routers import api

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api.router)
