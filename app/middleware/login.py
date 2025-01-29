from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class LoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ตรวจสอบว่า request มีข้อมูลการ login หรือไม่
        if 'user' not in request.state:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        response = await call_next(request)
        return response
