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

# backend/models/__init__.py

from ..core.database import Base

# Erst die unabhängigen Models importieren
from .fixtures import Manufacturer
from .shows import Show

# Dann die abhängigen Models
from .fixtures import FixtureType, FixtureChannel, Fixture

# Damit sind alle Klassen einmal geladen und bei "Base" registriert.
from .shows import Show, ShowAccess
from .dmx.scenes import Scene
from .dmx.cues import Cue
from .dmx.effects import CueEffect
from .dmx.effects import EffectTemplate
