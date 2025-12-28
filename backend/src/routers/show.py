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

from fastapi import APIRouter, Depends, status, HTTPException
from ..core.database import get_db
from ..core.security.access import require_programmer, require_operator
from ..schemas.show import CreateShow, GetShowfiles, GetShowfile
from ..services.shows import ShowService
import logging
import uuid

show_router = APIRouter(tags=["show"])

logger = logging.getLogger("AAAAAA")


@show_router.post("/api/shows")
async def post_create_show(
    create_show: CreateShow,
    db=Depends(get_db),
    current_user=Depends(require_programmer),
):
    logger.warning(current_user)
    show_service = ShowService(db)
    new_show = await show_service.create_showfile(create_show, current_user)
    return new_show

@show_router.get("/api/shows")
async def get_shows(page:int = 1, limit:int = 100, current_user=Depends(require_operator), db=Depends(get_db)):

    service = ShowService(db)
    showfiles = await service.get_showfiles(GetShowfiles(page=page, limit=limit, user=str(current_user.id)))
    return showfiles

@show_router.get("/api/show/{show_id}/patch")
async def get_patching(show_id:str, db=Depends(get_db), current_user=Depends(require_operator)):
    service = ShowService(db)
    patch = await service.get_patching(GetShowfile(user=str(current_user.id), id=str(show_id)))
    return patch