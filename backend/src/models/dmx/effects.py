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
from sqlalchemy import Column, UUID, JSON, String, Enum, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
import uuid
import enum


class FxTypes(enum.Enum):
    SINE = "sine"
    CHASER = "chaser"
    SPARKLE = "sparkle"


class EffectTemplate(Base):
    __tablename__ = "effect_templates"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(64), unique=True)
    fx_type = Column(Enum(FxTypes))

    default_parameters = Column(JSON, default=dict)


class CueEffect(Base):
    __tablename__ = "cue_effects"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    cue_id = Column(UUID, ForeignKey("cues.id", ondelete="CASCADE"))

    template_id = Column(UUID, ForeignKey("effect_templates.id"))

    fixture_group_id = Column(UUID, ForeignKey("fixture_groups.id"), nullable=False)

    parameters = Column(JSON, default=dict)

    template = relationship("EffectTemplate")
