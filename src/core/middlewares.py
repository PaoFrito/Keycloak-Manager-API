from fastapi import Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

class BaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next):      
        return await call_next(req)

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(BaseMiddleware)
]