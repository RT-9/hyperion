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

import enum
import uuid

from sqlalchemy import UUID, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ...core.database import Base


class TriggerType(enum.Enum):
    MANUAL = "manual"
    FOLLOW = "follow"


class EasingProfile(enum.Enum):
    LINEAR = "linear"
    S_CURVE = "s_curve"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"


class Cue(Base):
    __tablename__ = "cues"

    id = Column(UUID, primary_key=True, default=uuid.uuid7)
    show_id = Column(UUID, ForeignKey("shows.id"))

    scene_id = Column(UUID, ForeignKey("scenes.id"))

    number = Column(Integer, index=True)
    label = Column(String(64))
    hold = Column(Float, default=2, comment="Time to wait until next cue is loaded.")

    easing = Column(Enum(EasingProfile), default=EasingProfile.LINEAR)

    scene = relationship("Scene", back_populates="cues")
    show = relationship("Show", back_populates="cues")
    effects = relationship("CueEffect", backref="cue", cascade="all, delete-orphan")
