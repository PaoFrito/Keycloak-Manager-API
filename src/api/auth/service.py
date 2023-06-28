import asyncio
from typing import Dict
from .client import AuthClient

class AuthService():
    client:AuthClient = AuthClient()
    
    async def logout_user(self, user_id:str):
        asyncio.create_task(self._delete_sessions(await self.client.get_user_session_by_user_id(user_id=user_id)))
        
    async def _delete_sessions(self, sessions: Dict):
        for session in sessions:
            id = session['id']
            asyncio.create_task(self.client.delete_session_by_id(session_id=id))
