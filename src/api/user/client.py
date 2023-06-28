import asyncio
from typing import List
from pydantic import SecretStr
from fastapi_keycloak import KeycloakError, KeycloakUser, KeycloakGroup, KeycloakRole
from fastapi_keycloak.exceptions import UserNotFound
from ...core.exceptions import NotFoundException
from ...core.utils.dict_to_obj import dict2obj
from .schemas import KeycloakNewUser, UserEdit
from ...connections.keycloak_connection import idp
from ...connections.keycloak_connection import ConnectKeycloak

class UserClient(ConnectKeycloak):
    async def _keycloak(self, user_id: str,  method: str = "get", endpoint: str = "/", data = None):
        res = await asyncio.create_task(self._keycloak_request(method=method, url=f'users/{user_id}{endpoint}', data=data))
        return res
    
    # User  
    
    def get_all_users(self):
        return idp.get_all_users()
    
    def get_user_by_id(self, user_id: str) -> KeycloakUser:
        try:
            return idp.get_user(user_id=user_id)
        except UserNotFound as e:
            raise NotFoundException(f"User with id {user_id} was not found")
    
    def create_user(self, user: KeycloakNewUser):
        return idp.create_user(
            first_name              = user.first_name, 
            last_name               = user.last_name, 
            username                = user.username,
            email                   = user.email, 
            password                = user.password.get_secret_value(),
            send_email_verification = False
        ) 
        
    def update_user(self, user: KeycloakUser) -> KeycloakUser:
        res = idp.update_user(user=user)
        if isinstance(res, KeycloakUser):
            return res 
        raise KeycloakError(reason=f"{res}", status_code=500)

    def update_password(self, user_id: str, password: SecretStr) -> None:
        idp.change_password(user_id=user_id, new_password=password.get_secret_value())
        
    def delete_user(self, user_id: str) -> None:
        idp.delete_user(user_id=user_id)
    
    # Group
    
    def get_user_groups(self, user_id: str) -> List[KeycloakGroup]:
        return idp.get_user_groups(user_id=user_id)
    
    def add_user_to_group(self, user_id: str, group_id: str) -> List[KeycloakGroup]:
        idp.add_user_group(user_id=user_id, group_id=group_id)
        return self.get_user_groups(user_id=user_id)
    
    def remove_user_from_group(self, user_id: str, group_id: str) -> List[KeycloakGroup]:
        idp.remove_user_group(user_id=user_id, group_id=group_id)
        return self.get_user_groups(user_id=user_id)
        

    # Role
    
    async def get_user_efective_roles(self, user_id: str) -> List[KeycloakRole]:
        return dict2obj(await asyncio.create_task(self._keycloak(user_id=user_id, endpoint='/role-mappings/realm/composite')), KeycloakRole)