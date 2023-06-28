import asyncio
from fastapi_keycloak import KeycloakGroup, KeycloakRole
from typing import List
from ...core.exceptions import BadRequestException, NotFoundException
from .client import GroupClient
from .schemas import GroupList

class GroupService():
	client:GroupClient = GroupClient()
 
	def get_all_groups(self) -> List[KeycloakGroup]:
		return self.client.get_all_groups()

	def get_groups_by_name(self, groups: GroupList) -> List[KeycloakGroup]:
		if not groups.groups:
			raise BadRequestException("group_name_list can not be empty")
		res = self.client.get_groups_by_name(group_name_list=groups.groups)
		if not res:
			raise NotFoundException("No group was found")
		return res

	async def get_group_by_id(self, group_id: str) -> KeycloakGroup:
		if group_id == "":
			raise BadRequestException("group_id can not be empty")
		return await asyncio.create_task(self.client.get_group_by_id(group_id))
	
	async def get_group_members(self, group_id: str):
		return await asyncio.create_task(self.client.get_group_members(group_id))

	async def get_group_roles(self, group_id: str) -> List[KeycloakRole]:
		return await asyncio.create_task(self.client.get_group_roles(group_id))