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

from sqlalchemy import JSON, UUID, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from ...core.database import Base


class FxTypes(enum.Enum):
    """
    Define the algorithmic behaviour for dynamic lighting effects.

    This enumeration categorises the different generators used to manipulate 
    fixture attributes over time. Each type implements a distinct logic 
    for value distribution across one or multiple fixtures.

    :cvar SINE: A periodic oscillation based on a sinusoidal wave. 
        Typically used for smooth, continuous fading or gentle movement 
        swinging around a central point.
    :cvar CHASER: A sequential step-based effect where values 'travel' 
        across a selection of fixtures in a specific order. Useful for 
        creating directional movement or rhythmic patterns.
    :cvar SPARKLE: A stochastic effect that triggers brief, high-intensity 
        flashes at random intervals across the fixture selection. 
        Simulates a shimmering or 'glitter' aesthetic.
    """
    SINE = "sine"
    CHASER = "chaser"
    SPARKLE = "sparkle"


class EffectTemplate(Base):
    """
    Define a reusable blueprint for lighting effects within the system.

    Effect templates store the logic and baseline configuration for dynamic 
    behaviours. By using a template, users can maintain consistency across 
    different shows while only overriding specific parameters where necessary.

    The template links a high-level :class:`FxTypes` algorithm with a 
    set of default configuration variables stored in a flexible JSON format.

    :param id: Unique identifier for the template, utilising UUID v7.
    :type id: uuid.UUID
    :param name: A unique, human-readable identifier for the template 
        (e.g., "Fast Blue Strobe").
    :type name: str
    :param fx_type: The underlying mathematical algorithm used by this 
        template.
    :type fx_type: FxTypes
    :param default_parameters: A dictionary of key-value pairs representing 
        algorithm-specific settings such as 'frequency', 'phase', 
        or 'intensity_range'.
    :type default_parameters: dict
    """
    __tablename__ = "effect_templates"
    id = Column(UUID, primary_key=True, default=uuid.uuid7)
    name = Column(String(64), unique=True)
    fx_type = Column(Enum(FxTypes))

    default_parameters = Column(JSON, default=dict)


class CueEffect(Base):
    """
    Represent the application of an effect template to a specific cue.

    This class acts as an intersection between a :class:`Cue` and an 
    :class:`EffectTemplate`. It allows for the customisation of effect 
    parameters on a per-cue basis, enabling the same template to be 
    utilised with different speeds, intensities, or colours throughout 
    a show.

    The relationship ensures that when a cue is triggered, the associated 
    algorithmic effects are initialised with the correct overridden 
    parameters.

    :param id: Unique identifier for this specific effect instance.
    :type id: uuid.UUID
    :param cue_id: Reference to the parent :class:`Cue`. 
        Uses 'CASCADE' on delete to ensure orphaned effects are removed.
    :type cue_id: uuid.UUID
    :param template_id: Reference to the underlying :class:`EffectTemplate` 
        utilised for this effect.
    :type template_id: uuid.UUID
    :param parameters: A JSON object containing parameter overrides. These 
        values take precedence over the `default_parameters` defined in the 
        associated template.
    :type parameters: dict
    """
    __tablename__ = "cue_effects"
    id = Column(UUID, primary_key=True, default=uuid.uuid7)

    cue_id = Column(UUID, ForeignKey("cues.id", ondelete="CASCADE"))

    template_id = Column(UUID, ForeignKey("effect_templates.id"))

    # fixture_group_id = Column(UUID, ForeignKey("fixture_groups.id"), nullable=False)

    parameters = Column(JSON, default=dict)

    template = relationship("EffectTemplate")
