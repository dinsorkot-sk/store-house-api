from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class LoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not hasattr(request.state, "user"):  # Fixed check
            request.state.user = None  # Ensure `user` exists
        response = await call_next(request)
        return response
