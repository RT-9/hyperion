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

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    JWT_SECRET: str
    HOST: str = "127.0.0.1"
    PORT: int = 2468
    DEBUG: bool = False
    MARIADB_USER: str = "hyperion"
    MARIADB_PASSWORD: str = "hyperion"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DATABASE: str = "hyperion"
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")
    DROP_DB: bool = False

    @property
    def db_url(self):
        return f"mysql+asyncmy://{self.MARIADB_USER}:{self.MARIADB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE}"
