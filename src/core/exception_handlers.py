from typing import Dict
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_keycloak import KeycloakError
from jose import ExpiredSignatureError, JWTError
from .exceptions import NotFoundException, BadRequestException, UnauthorizedException
from .http_responses import error_responses

async def expired_signature_error_handler(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(
        status_code=error_responses[401]['code'],
        content={"error": "Token expired"}
    )
    
async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=error_responses[401]['code'],
        content={"error": "Invalid token"}
    )
    
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code = error_responses[401]['code'],
        content = {"error": exc.text}
    )
    
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code = error_responses[404]['code'],
        content = {"error": exc.text}
    )
    
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code = error_responses[400]['code'],
        content = {"error": exc.text}
    )
    
async def keycloak_error_handler(request: Request, exc: KeycloakError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": f"{exc.reason}"}
    )

async def error_handler(request: Request, exc: Exception):
    msg = exc.args if exc.args != "" else error_responses[500]['description']
    return JSONResponse(
        status_code = error_responses[500]['code'],
        content = {"error": f"{msg}"}
    )

exception_handlers: Dict = {
    ExpiredSignatureError:expired_signature_error_handler,
    JWTError: jwt_error_handler,
    NotFoundException: not_found_exception_handler,
    BadRequestException: bad_request_exception_handler,
    UnauthorizedException: unauthorized_exception_handler,
    KeycloakError: keycloak_error_handler,
    Exception: error_handler
}