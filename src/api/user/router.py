import asyncio
from fastapi import APIRouter, Depends
from fastapi_keycloak import OIDCUser, KeycloakUser, KeycloakGroup, KeycloakRole
from typing import List
from ...core.http_responses import success_responses
from .service import UserService
from ..group.service import GroupService
from .dependencies import user_group_ids
from .schemas import (
    NewUser, 
    KeycloakUserGroup,
    UserEdit,
    UserChangePassword,
    UserGroup
)

router = APIRouter(prefix="/user")
service:UserService = UserService()
group_service:GroupService = GroupService()

# User
user_router = APIRouter(tags=["User"])

# Get all users
@user_router.get("/")
async def get_all_users() -> List[KeycloakUser]:
    return service.get_all_users()

# Get user by id
@user_router.get("/{user_id}")
async def get_user_by_id(user: KeycloakUser = Depends(service.get_user_by_id)) -> KeycloakUser:
    return user

@user_router.post("/", status_code=201, responses={201: success_responses[201]})
async def create_user(user: NewUser) -> KeycloakUserGroup:
    return service.create_user(new_user=user)

@user_router.put("/{user_id}")
async def update_user(user:UserEdit, curr_user: KeycloakUser = Depends(service.get_user_by_id)) -> KeycloakUser:
    return service.update_user(curr_user=curr_user, new_user_data=user)

@user_router.put("/update-password")
async def update_password(user: UserChangePassword) -> None:
    service.update_password(user_id=user.id, password=user.new_password)
    
@user_router.delete("/{user_id}", status_code=204, responses={204: success_responses[204]})
async def hard_delete_user(user: KeycloakUser = Depends(service.get_user_by_id)) -> None:
    service.hard_delete_user(user_id=user.id)
        
@user_router.delete("/disable/{user_id}")
async def soft_delete_user(user: KeycloakUser = Depends(service.get_user_by_id)) -> KeycloakUser:
    return service.soft_delete_user(user=user)

@user_router.put("/enable/{user_id}")
async def restore_user(user: KeycloakUser = Depends(service.get_user_by_id)) -> KeycloakUser:
    return service.enable_user(user=user)

# User Group
group_router = APIRouter(prefix="/group",tags=["User-Group"])

# Get User Groups
@group_router.get("/{user_id}")
async def get_user_groups(user: KeycloakUser = Depends(service.get_user_by_id)) -> List[KeycloakGroup]:
    return service.get_user_groups(user_id=user.id)

# Add User to Group
@group_router.post("/")
async def add_user_to_group(data: UserGroup = Depends(user_group_ids)) -> List[KeycloakGroup]:
    return service.add_user_to_group(user_id=data.user_id, group_id=data.group_id)
    
# Remove User from Group
@group_router.delete("/")
async def remove_user_from_group(data: UserGroup = Depends(user_group_ids)) -> List[KeycloakGroup]:
    return service.remove_user_from_group(user_id=data.user_id, group_id=data.group_id)
    
# User Role
role_router = APIRouter(prefix="/role", tags=["User-Role"])

@role_router.get("/{user_id}")
async def get_user_roles(user: KeycloakUser = Depends(service.get_user_by_id)) -> List[KeycloakRole]:
    return await asyncio.create_task(service.get_user_efective_roles(user_id=user.id))

router.include_router(user_router)
router.include_router(group_router)
router.include_router(role_router)