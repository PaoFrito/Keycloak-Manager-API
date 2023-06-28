import asyncio
from typing import List
from fastapi import APIRouter, Depends
from fastapi_keycloak import KeycloakGroup
from ...connections.keycloak_connection import idp
from .service import GroupService
from .schemas import NewGroup, GroupList
from ...core.http_responses import success_responses

router = APIRouter(
        prefix="/groups", 
        tags=["Groups"]
    )
service: GroupService = GroupService()

# Get all groups
@router.get("/")
async def get_all_groups() -> List[KeycloakGroup]:
    return service.get_all_groups()

# Get groups by name
@router.get("/name")
async def get_group(group_name_list: GroupList) -> List[KeycloakGroup]:
    return service.get_groups_by_name(groups=group_name_list)

# Get group by id
@router.get("/{group_id}")
async def get_group_by_id(group: KeycloakGroup = Depends(service.get_group_by_id)) -> KeycloakGroup:
    return group

# Get group members
@router.get("/{group_id}/members")
async def get_group_members(group: KeycloakGroup = Depends(service.get_group_by_id)) :
    return await asyncio.create_task(service.get_group_members(group_id=group.id))

# Get group roles
@router.get("/{group_id}/roles")
async def get_group_roles(group: KeycloakGroup = Depends(service.get_group_by_id)):
    return await asyncio.create_task(service.get_group_roles(group_id=group.id))

# Create group
@router.post("/", 
    status_code=201,
    responses={
        201: success_responses[201]
})
async def add_group(group: NewGroup) -> KeycloakGroup:
    return idp.create_group(group_name=group.name)
 
# Delete group
@router.delete("/{group_id}", status_code=204, responses={204: success_responses[204]})
async def delete_groups(group: KeycloakGroup = Depends(service.get_group_by_id)):
    idp.delete_group(group_id=group.id)
    return None