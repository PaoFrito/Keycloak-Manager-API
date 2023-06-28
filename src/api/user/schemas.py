from fastapi_keycloak import KeycloakUser, KeycloakGroup
from pydantic import BaseModel, SecretStr, Field, EmailStr, validator
from typing import Optional, List
from ..group.service import GroupService
from ...core.exceptions import BadRequestException 

class NewUser(BaseModel):
    _group_service:GroupService = GroupService()
    
    username:str = Field(min_length=3, max_length=50, regex="^[A-Za-z]+$")
    email: EmailStr
    password: SecretStr = Field(min_length=6, max_length=32)
    repeat_password: SecretStr
    first_name:str = Field(min_length=3, max_length=32, regex="^[A-Za-z]+$")
    last_name:str = Field(default=None, min_length=3, max_length=32, regex="^[A-Za-z]+$")
    group_id: str
    
    @validator('repeat_password')
    def validate_repeat_password(cls, v, values, **kwargs):
        if 'password' in values and v.get_secret_value() != values['password'].get_secret_value():
            raise BadRequestException('Passwords do not match')
        return v

class KeycloakUserGroup(BaseModel):
    user:KeycloakUser
    group:List[KeycloakGroup] = Field(default=None)

class KeycloakNewUser(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr
    first_name: str
    last_name: str
    
class UserChangePassword(BaseModel):
    id: str
    new_password: SecretStr
    repeat_new_password: SecretStr

    @validator('repeat_new_password')
    def validate_repeat_password(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise BadRequestException('Passwords do not match')
        return v
    
class UserEdit(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str

class UserGroup(BaseModel):
    user_id: str
    group_id: str
    
class UserRole(BaseModel):
    user_id: str
    roles: List[str]    