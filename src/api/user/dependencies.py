import asyncio
from .schemas import UserGroup
from ..group.service import GroupService
from .service import UserService

async def user_group_ids(user_group: UserGroup) -> UserGroup:
    user_service:UserService = UserService()
    group_service:GroupService = GroupService()
    
    user_service.get_user_by_id(user_group.user_id)
    res = await asyncio.create_task(group_service.get_group_by_id(user_group.group_id))
    return user_group