import asyncio
from fastapi_keycloak import FastAPIKeycloak
from .request import request
from core.exceptions import NotFoundException
from core.config import ADMIN_CLIENT_ID, ADMIN_CLIENT_SECRET, KEYCLOAK_URL, API_URL, REALM_NAME, CLIENT_ID, CLIENT_SECRET

idp = FastAPIKeycloak(
    server_url          = KEYCLOAK_URL,
    client_id           = CLIENT_ID,
    client_secret       = CLIENT_SECRET,
    admin_client_secret = ADMIN_CLIENT_SECRET,
    realm               = REALM_NAME,
    callback_uri        = API_URL + "/callback"
)

class ConnectKeycloak():
    async def _get_token(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": ADMIN_CLIENT_ID,
            "client_secret": ADMIN_CLIENT_SECRET
        }   
        
        return request(method='post', url=f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token", data=data).json()["access_token"]
    
    async def _keycloak_request(self, method: str, url: str, data = None):
        task = asyncio.create_task(self._get_token())        
        headers = { "Authorization": f"Bearer {await task}" }
        res = request(method=method, url=f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/{url}", headers=headers, data=data).json()
        if 'error' in res:
            raise NotFoundException(res['error'])
        return res