import asyncio
from fastapi import APIRouter, Depends
from fastapi_keycloak import KeycloakRole
from ...connections.keycloak_connection import idp
from ...core.http_responses import success_responses
from .schemas import Role, RoleNameList
from .service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])
service:RoleService = RoleService() 

# Get All Roles
@router.get("/")
async def get_all_roles():
    return idp.get_all_roles()

# Get Role by Name
@router.get("/name")
async def get_role_by_name(roles: RoleNameList):    
    return service.get_roles_by_name(roles=roles)

# Get Role by ID
@router.get("/{role_id}")
async def get_role_by_id(role: KeycloakRole = Depends(service.get_role_by_id)):
    return role

# Create Role
@router.post("/")
async def add_role(new_role: Role):    
    return service.create_role(role_name=new_role.name)

# Delete Role by name
@router.delete("/name/{role_name}", status_code=204, responses={204: success_responses[204]})
async def delete_role_by_name(role_name: str):    
    service.delete_role_by_name(role_name=role_name)
    return None

# Delete Role by id
@router.delete("/{role_id}", status_code=204, responses={204: success_responses[204]})
async def delete_role_by_id(role: KeycloakRole = Depends(service.get_role_by_id)):    
    asyncio.create_task(service.delete_role_by_id(role_id=role.id))
    return None 