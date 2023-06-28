from fastapi_keycloak import KeycloakGroup
from typing import Optional, List, Any
from pydantic import BaseModel

class GroupList(BaseModel):
    groups: List[str]

class NewGroup(BaseModel):
    name: str