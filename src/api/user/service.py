import asyncio
from fastapi_keycloak import KeycloakUser, KeycloakGroup, KeycloakRole
from typing import Dict, List
from pydantic import SecretStr
from ...core.exceptions import NotFoundException, BadRequestException
from ..group.service import GroupService
from .client import UserClient
from .schemas import NewUser, KeycloakUserGroup, KeycloakNewUser, UserEdit

class UserService():
    client:UserClient = UserClient()
    
    def get_all_users(self) -> list[KeycloakUser]:
        return self.client.get_all_users()
    
    def get_user_by_id(self, user_id: str) -> KeycloakUser:
        if user_id == "":
            raise BadRequestException("User id is required")
        return self.client.get_user_by_id(user_id=user_id)

    def create_user(self, new_user: NewUser) -> KeycloakUserGroup:
        
        user:KeycloakNewUser = KeycloakNewUser(
            username=new_user.username,
            email=new_user.email,
            password=new_user.password,
            first_name=new_user.first_name,
            last_name=new_user.last_name
        )
        created_user:KeycloakUser = self.client.create_user(user=user)
        
        groups = []
        if new_user.group_id != "":
            try:
                groups = self.client.add_user_to_group(user_id=created_user.id, group_id=new_user.group_id)
            except Exception:
                print("Error adding user to group")

        return KeycloakUserGroup(
            user=created_user,
            group=groups
        )
    
    def update_user(self, curr_user: KeycloakUser, new_user_data: UserEdit) -> KeycloakUser:
        if curr_user.id != new_user_data.id:
            raise BadRequestException("Inconsistent user id")
        
        curr_user.username = new_user_data.username
        curr_user.email = new_user_data.email
        curr_user.first_name = new_user_data.first_name
        curr_user.last_name = new_user_data.last_name
        
        return self.client.update_user(user=curr_user)
    
    def update_password(self, user_id: str, password: SecretStr) -> None:
        self.get_user_by_id(user_id=user_id)
        self.client.update_password(user_id=user_id, password=password)
    
    def hard_delete_user(self, user_id: str) -> None:
        self.client.delete_user(user_id=user_id)
        
    def soft_delete_user(self, user: KeycloakUser) -> KeycloakUser:
        user.enabled = False
        return self.client.update_user(user=user)
    
    def enable_user(self, user: KeycloakUser) -> KeycloakUser:
        user.enabled = True
        return self.client.update_user(user=user)
    
    # User Groups
    
    def get_user_groups(self, user_id: str) -> List[KeycloakGroup]:
        return self.client.get_user_groups(user_id=user_id)
    
    def add_user_to_group(self, user_id: str, group_id: str) -> List[KeycloakGroup]:   
        return self.client.add_user_to_group(user_id=user_id, group_id=group_id)
    
    def remove_user_from_group(self, user_id: str, group_id: str) -> List[KeycloakGroup]:
        return self.client.remove_user_from_group(user_id=user_id, group_id=group_id)

    # User Roles
    async def get_user_efective_roles(self, user_id: str) -> List[KeycloakRole]:
        return await asyncio.create_task(self.client.get_user_efective_roles(user_id=user_id))