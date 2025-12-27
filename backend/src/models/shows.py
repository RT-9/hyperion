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
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Table,
    Boolean,
    DateTime,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from ..core.database import Base, TimestampMixin


class Show(Base, TimestampMixin):
    """
    Represents a lighting show file.

    :param id: User-friendly integer identifier
    :param name: Unique name of the show
    :param created_by: Reference to the account that created the show
    :param description: Optional details about the production
    """

    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    created_by = Column(ForeignKey("accounts.id"), nullable=False)
    description = Column(String, nullable=True)

    fixtures = relationship(
        "Fixture", back_populates="show", cascade="all, delete-orphan"
    )
