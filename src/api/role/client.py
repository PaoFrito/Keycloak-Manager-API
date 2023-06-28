import asyncio
from typing import List
from fastapi_keycloak import KeycloakRole
from ...core.utils.dict_to_obj import dict2obj
from ...connections.keycloak_connection import ConnectKeycloak
from ...connections.keycloak_connection import idp

class RoleClient(ConnectKeycloak):
    async def _keycloak(self, role_id: str,  method: str = "get", endpoint: str = "/", data = None):
        res = await asyncio.create_task(self._keycloak_request(method=method, url=f'roles-by-id/{role_id}{endpoint}', data=data))
        return res

    async def get_role_by_id(self, role_id: str) -> KeycloakRole:
        res = await asyncio.create_task(self._keycloak(role_id=role_id)) 
        res = dict2obj(res, KeycloakRole)
        return res

    async def delete_role_by_id(self, role_id: str) -> None:
        await asyncio.create_task(self._keycloak(role_id=role_id, method="delete"))
        
    def get_roles_by_name(self, roles:List[str]) -> List[KeycloakRole] | None:
        return idp.get_roles(role_names=roles)
    
    def create_role(self, role_name: str) -> KeycloakRole:
        return idp.create_role(role_name=role_name)
    
    def delete_role_by_name(self, role_name: str) -> None:
        idp.delete_role(role_name=role_name)