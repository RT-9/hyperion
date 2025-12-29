# Hyperion
# Copyright (C) 2025 Arian Ott <arian.ott@ieee.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models.accounts import Accounts, Role

logger = logging.getLogger("hyperion.startup.service")


class StartupService:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def admin_created(self):
        try:
            qry = (
                select(func.count())
                .where(Accounts.role_id == Role.id)
                .where(Role.name == "admin")
            )
            result = await self.db.execute(qry)
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(str(e))
            raise
        return result.scalar()

    async def check_initial_procedure(self):
        if user_count := await self.admin_created():
            logger.info(f"{user_count} admin accounts already exist")
            return False
            
        return True
