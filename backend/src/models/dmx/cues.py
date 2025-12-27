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
from sqlalchemy import Column, UUID, Integer, String, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import uuid
import enum


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

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    show_id = Column(UUID, ForeignKey("shows.id"))

    scene_id = Column(UUID, ForeignKey("scenes.id"))

    number = Column(Float, index=True)
    label = Column(String(64))
    fade_in = Column(Float, default=2.0)
    trigger = Column(Enum(TriggerType), default=TriggerType.MANUAL)
    trigger_value = Column(Float, default=0.0)
    easing = Column(Enum(EasingProfile), default=EasingProfile.LINEAR)
    next_cue_id = Column(UUID, ForeignKey("cues.id"), nullable=True)
    is_loop_end = Column(Boolean, default=False)
    scene = relationship("Scene", back_populates="cues")
    show = relationship("Show", back_populates="cues")
    effects = relationship("CueEffect", backref="cue", cascade="all, delete-orphan")
