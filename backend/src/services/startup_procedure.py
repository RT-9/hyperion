from sqlalchemy.ext.asyncio import AsyncSession
from ..models.accounts import Accounts, Role
from sqlalchemy import select, exists, func

import logging 

logger = logging.getLogger("startup.service")

class StartupService:
    
    def __init__(self, session: AsyncSession):
        self.db = session 
        
    async def admin_created(self):
        qry = (
            select(func.count())
            .where(Accounts.role_id == Role.id)
            .where(Role.name == "admin")
        )
        result = await self.db.execute(qry)
        return result.scalar()
    
    
    
    async def check_initial_procedure(self):
        if user_count := await self.admin_created():
            logger.info(f"{user_count} admin accounts already exist")
            return False 
        return True