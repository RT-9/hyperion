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

import uuid

from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ...core.database import Base
from ..fixtures import AttributeType


class Scene(Base):
    __tablename__ = "scenes"
    id = Column(UUID, primary_key=True, default=uuid.uuid7)

    sid = Column(Integer, index=True, nullable=False)
    name = Column(String(32), nullable=True)
    show_id = Column(
        UUID(as_uuid=True), ForeignKey("shows.id", ondelete="CASCADE"), nullable=False
    )
    show = relationship("Show", back_populates="scenes")
    cues = relationship("Cue", back_populates="scene", cascade="all, delete-orphan")
    fixture_associations = relationship(
        "SceneFixtureValue",
        back_populates="scene",
        cascade="all, delete-orphan",  # Wenn Szene gelöscht wird, lösche auch die Werte
        lazy="selectin",  # WICHTIG: Lädt die Daten sofort effizient mit
    )


class SceneFixtureValue(Base):
    """
    Speichert EINEN Wert für EINEN Kanal eines Geräts in einer Szene.
    Ersetzt das alte JSON-Blob Konzept durch sauberes SQL.
    """

    __tablename__ = "scene_fixture_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)

    scene_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scenes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    fixture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("fixtures.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    attribute = Column(Enum(AttributeType), nullable=False)

    value = Column(Integer, nullable=False)

    scene = relationship("Scene", back_populates="fixture_associations")

    fixture = relationship("Fixture", lazy="joined")
