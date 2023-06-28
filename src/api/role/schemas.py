from fastapi_keycloak import KeycloakRole
from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    name: str

class RoleNameList(BaseModel):
    role_name: List[str]

class RoleMappins():
    realmMappings: List[KeycloakRole]