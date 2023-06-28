from fastapi import APIRouter, Depends
from api.auth.router import router as auth_router
from api.user.router import router as user_router
from api.group.router import router as group_router
from api.role.router import router as role_router
from connections.keycloak_connection import idp

router = APIRouter()

router.include_router(auth_router)

# Protected routes
protected_router = APIRouter()#dependencies=[Depends(idp.get_current_user())])
protected_router.include_router(user_router)
protected_router.include_router(group_router)
protected_router.include_router(role_router)

router.include_router(protected_router)