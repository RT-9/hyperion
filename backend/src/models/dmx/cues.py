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
from sqlalchemy import Column, UUID, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import uuid
import enum


class TriggerType(enum.Enum):
    MANUAL = "manual"
    FOLLOW = "follow"


class Cue(Base):
    __tablename__ = "cues"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    show_id = Column(UUID, ForeignKey("shows.id"))

    scene_id = Column(UUID, ForeignKey("scenes.id"))

    number = Column(Float, index=True)
    label = Column(String(64))
    fade_in = Column(Float, default=2.0)
    trigger = Column(Enum(TriggerType), default=TriggerType.MANUAL)

    scene = relationship("Scene", back_populates="cues")

    effects = relationship("CueEffect", backref="cue", cascade="all, delete-orphan")
