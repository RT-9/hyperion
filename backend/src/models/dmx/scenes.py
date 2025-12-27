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

from ...core.database import Base
from sqlalchemy import UUID, Integer, ForeignKey, Column, String, JSON
from sqlalchemy.orm import relationship
import uuid


class Scene(Base):
    __tablename__ = "scenes"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    sid = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=True)

    show_id = Column(UUID, ForeignKey("shows.id"))

    dmx_data = Column(JSON, default=dict)

    cues = relationship("Cue", back_populates="scene")
    show = relationship("Show", back_populates="scenes")
