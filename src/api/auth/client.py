import asyncio
from ...connections.keycloak_connection import ConnectKeycloak

class AuthClient(ConnectKeycloak): 

    async def get_user_session_by_user_id(self, user_id:str) -> dict:
        sessions = await asyncio.create_task(self._keycloak_request(method='get', url=f'users/{user_id}/sessions'))
        return sessions
    
    async def delete_session_by_id(self, session_id:str):
        await asyncio.create_task(self._keycloak_request(method='delete', url=f'sessions/{session_id}'))