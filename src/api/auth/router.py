import asyncio
from fastapi import APIRouter, Depends
from fastapi_keycloak import UsernamePassword, KeycloakToken
from connections.keycloak_connection import idp
from core.http_responses import success_responses
from .service import AuthService

router = APIRouter(tags=["Authentication"])
auth_service:AuthService = AuthService()

@router.post('/login')
async def login(user: UsernamePassword) -> KeycloakToken:
    return idp.user_login(username=user.username, password=user.password.get_secret_value())

@router.delete("/logout", status_code=204, responses={204: success_responses[204]})
async def logout(user = Depends(idp.get_current_user(extra_fields=["sub"]))):    
    """ Header needs to have a valid token """
    id = user.extra_fields["sub"]
    asyncio.create_task(auth_service.logout_user(user_id=id))
    return None