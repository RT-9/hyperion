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
    """
    Define the mechanism used to initiate the transition to the next cue.

    This enumeration determines whether the sequence progression requires 
    human intervention or is handled automatically by the system clock.

    :cvar MANUAL: The cue remains active until a manual 'Go' command is 
        received from the operator or an external trigger.
    :cvar FOLLOW: The next cue is automatically triggered once the current 
        cue's hold and fade durations have elapsed.
    """
    MANUAL = "manual"
    FOLLOW = "follow"


class EasingProfile(enum.Enum):
    """
    Specify the mathematical interpolation curve for lighting transitions.

    Easing profiles control the rate of change for DMX channel values over 
    time, allowing for more natural or stylised movement and intensity fades.

    :math:`v(t) = f(t)` where :math:`t` is normalised time [0, 1].

    :cvar LINEAR: A constant rate of change. Ideal for utilitarian 
        transitions.
    :cvar S_CURVE: Slow start and end with a fast middle section. Provides 
        the most natural aesthetic for moving lights.
    :cvar EASE_IN: Starts slowly and accelerates towards the end of the 
        transition.
    :cvar EASE_OUT: Starts quickly and decelerates towards the target value.
    """
    LINEAR = "linear"
    S_CURVE = "s_curve"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"


class Cue(Base):
    """Represent a specific lighting state or command within a show sequence.

    A Cue is a discrete point in a performance's timeline. It links a static 
    lighting :class:`Scene` or dynamic :class:`CueEffect` to a specific 
    chronological order within a :class:`Show`. It manages the transition 
    logic, such as timing and easing profiles, between different states.

    In the context of the Hyperion system, a Cue acts as the orchestrator 
    that determines when and how a scene should be realised on the 
    physical fixtures.
    
    :param id: Unique identifier for the cue, using UUID v7 for sortable 
        uniqueness.
    :type id: uuid.UUID
    :param show_id: Foreign key associating this cue with a specific show.
    :type show_id: uuid.UUID
    :param scene_id: Foreign key linking to the visual scene to be triggered.
    :type scene_id: uuid.UUID
    :param number: The numerical order of the cue within the show's sequence.
    :type number: int
    :param label: A human-readable description or name for the cue.
    :type label: str
    :param hold: The duration in seconds to maintain the current state 
        before the next cue is eligible for triggering. Defaults to 2.0.
    :type hold: float
    :param easing: The mathematical profile used to transition values (e.g. 
        Linear, Ease-In, Ease-Out).
    :type easing: EasingProfile
    """
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
