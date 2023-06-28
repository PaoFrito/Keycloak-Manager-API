import asyncio
from typing import List
from fastapi_keycloak import KeycloakGroup, KeycloakRole
from src.core.utils.dict_to_obj import dict2obj
from ..role.schemas import RoleMappins
from ...connections.keycloak_connection import idp
from ...connections.keycloak_connection import ConnectKeycloak

class GroupClient(ConnectKeycloak):
    async def _keycloak(self, group_id: str,  method: str = "get", endpoint: str = "/"):
        res = await asyncio.create_task(self._keycloak_request(method=method, url=f'groups/{group_id}{endpoint}'))
        return res
        
    def get_all_groups(self) -> List[KeycloakGroup]:
        return idp.get_all_groups()

    def get_groups_by_name(self, group_name_list: List[str]):
        return idp.get_groups(group_name_list)

    async def get_group_by_id(self, group_id: str) -> KeycloakGroup:
        res:KeycloakGroup = await asyncio.create_task(self._keycloak(group_id=group_id))
        res = dict2obj(res, KeycloakGroup)
        return res
    
    async def get_group_members(self, group_id: str):
        res = await asyncio.create_task(self._keycloak(group_id=group_id, endpoint="/members"))
        return res

    async def get_group_roles(self, group_id: str) -> List[KeycloakRole]:
        res:RoleMappins = await asyncio.create_task(self._keycloak(group_id=group_id, endpoint="/role-mappings"))
        res = dict2obj(res, RoleMappins)
        roles:List[KeycloakRole] = res.realmMappings
        return roles