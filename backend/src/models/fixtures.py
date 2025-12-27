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
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base  # Pfad ggf. anpassen




class AttributeType(str, enum.Enum):
    """
    Defines the possible types of DMX attributes.
    Used for type safety and mapping logic in the engine.
    """
    DIMMER = "dimmer"
    STROBE = "strobe"
    SHUTTER = "shutter"


    PAN = "pan"
    PAN_FINE = "pan_fine"
    TILT = "tilt"
    TILT_FINE = "tilt_fine"

    COLOR_RED = "color_red"
    COLOR_GREEN = "color_green"
    COLOR_BLUE = "color_blue"
    COLOR_WHITE = "color_white"
    COLOR_WHEEL = "color_wheel"

    FOG = "fog"
    FAN = "fan"
    SPEED = "speed"

    # Placeholder
    UNKNOWN = "unknown"


class Manufacturer(Base):
    """
    Represents a manufacturer of lighting fixtures (e.g. Clay Paky, Robe, Stairville).
    """
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)

    website = Column(String(200), nullable=True)


    fixture_types = relationship("FixtureType", back_populates="manufacturer")

    def __repr__(self):
        return f"<Manufacturer {self.name}>"



class FixtureType(Base):
    """
    Defines the blueprint/profile of a specific fixture model (e.g. Stairville HZ-200).
    Links a manufacturer to specific DMX channels.
    """
    __tablename__ = "fixture_types"

    id = Column(Integer, primary_key=True, index=True)


    manufacturer_id = Column(Integer, ForeignKey(
        "manufacturers.id"), nullable=False)

    model = Column(String(100), nullable=False)        
    mode_name = Column(String(50), default="Standard") 

   
    manufacturer = relationship(
        "Manufacturer", back_populates="fixture_types", lazy="joined")

   
    channels = relationship(
        "FixtureChannel",
        back_populates="fixture_type",
        cascade="all, delete-orphan",
        lazy="selectin"  # Async-Optimierung
    )

    
    instances = relationship("Fixture", back_populates="fixture_type")

    def __repr__(self):
      
        manufacturer_name = self.manufacturer.name if self.manufacturer else "Unknown"
        return f"<FixtureType {manufacturer_name} {self.model} ({self.mode_name})>"



class FixtureChannel(Base):
    """
    Maps a logical attribute (e.g. FOG) to a DMX offset for a specific FixtureType.
    """
    __tablename__ = "fixture_channels"

    id = Column(Integer, primary_key=True, index=True)
    fixture_type_id = Column(Integer, ForeignKey(
        "fixture_types.id"), nullable=False)

    dmx_offset = Column(Integer, nullable=False)
    attribute = Column(Enum(AttributeType), nullable=False)
    default_value = Column(Integer, default=0)
    highlight_value = Column(Integer, default=255)
    invert_default = Column(Boolean, default=False)

    fixture_type = relationship("FixtureType", back_populates="channels")



class Fixture(Base):
    """
    Represents a concrete physical device patched in the DMX universe.
    """
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    fixture_type_id = Column(Integer, ForeignKey(
        "fixture_types.id"), nullable=False)

    universe = Column(Integer, default=0, nullable=False)
    start_address = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    invert_pan = Column(Boolean, default=False)
    invert_tilt = Column(Boolean, default=False)

    fixture_type = relationship(
        "FixtureType", back_populates="instances", lazy="selectin")

    def __repr__(self):
        return f"<Fixture '{self.name}' @ U{self.universe}.{self.start_address}>"
