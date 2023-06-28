import asyncio
from typing import List
from fastapi_keycloak import KeycloakRole
from .client import RoleClient
from .schemas import RoleNameList
from ...core.exceptions import BadRequestException, NotFoundException

class RoleService():
    client: RoleClient = RoleClient()
    
    async def get_role_by_id(self, role_id: str) -> KeycloakRole:
        if role_id == "":
            raise BadRequestException("role id can not be empty")
        return await asyncio.create_task(self.client.get_role_by_id(role_id=role_id))
        
    async def delete_role_by_id(self, role_id: str) -> None:
        asyncio.create_task(self.client.delete_role_by_id(role_id=role_id))
        
    def get_roles_by_name(self, roles:RoleNameList) -> List[KeycloakRole] | None:
        if not roles.role_name:
            raise BadRequestException("role list can not be empty")
        res = self.client.get_roles_by_name(roles=roles.role_name)
        if not res:
            raise NotFoundException("No role was found")
        return res
    
    def create_role(self, role_name: str) -> KeycloakRole:
        if role_name == "":
            raise BadRequestException("role name can not be empty")
        return self.client.create_role(role_name=role_name)
    
    def delete_role_by_name(self, role_name: str) -> None:
        self.client.delete_role_by_name(role_name=role_name)