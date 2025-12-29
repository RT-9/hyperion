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

from fastapi import APIRouter, Depends, HTTPException, status

from ..core.database import get_db
from ..core.exc import InvalidPasswordError
from ..schemas.accounts import UserCreate
from ..services.accounts import AccountService
from ..services.startup_procedure import StartupService

startup_router = APIRouter(tags=["startup"])


@startup_router.post("/api/startup/create-admin-user")
async def post_create_admin_user(user: UserCreate, db=Depends(get_db)):
    service = AccountService(db)
    user_count = await service.amount_users()
    if user_count >= 1:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Admin user already exists."
        )
    try:
        new_user = await service.create_user(user, role_name="admin")
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    return new_user


@startup_router.get("/api/startup/initial-procedure")
async def get_initial_procedure(db=Depends(get_db)):
    service = StartupService(db)
    result = await service.check_initial_procedure()
    return result
