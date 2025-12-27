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

import struct
import base64


class DMXProtocol:
    """
    Handles the binary packing of DMX data.

    Structure:
    - Bytes 0-1: Universe ID (Unsigned Short, 16-bit, Big Endian)
    - Bytes 2-N: Channel Values (Unsigned Char, 8-bit)
    """

    @staticmethod
    def pack_frame(universe: int, channels: list[int]) -> bytes:
        """
        Creates a binary DMX frame.

        :param universe: The DMX universe ID (0-65535).
        :param channels: A list of integer values (0-255) for the channels.
        :return: The packed binary frame.
        """
        # ! = Network (Big Endian)
        # H = Unsigned Short (2 Bytes) für Universum
        # B = Unsigned Char (1 Byte) pro Kanal
        # Das '*' entpackt die Liste in einzelne Argumente für struct.pack
        fmt = f"!H{len(channels)}B"
        return struct.pack(fmt, universe, *channels)

    @staticmethod
    def to_transport(universe: int, channels: list[int]) -> str:
        """
        Packs the frame and encodes it to Base64 for Redis transport.

        Since the Redis manager is set to decode_responses=True (Strings),
        we cannot send raw bytes directly without crashing the decoder.
        Base64 is the safe bridge.
        """
        binary_data = DMXProtocol.pack_frame(universe, channels)
        # Return as string for Redis
        return base64.b64encode(binary_data).decode("utf-8")

    @staticmethod
    def from_transport(b64_data: str) -> bytes:
        """
        Decodes the Base64 string back to raw bytes for the WebSocket.
        """
        return base64.b64decode(b64_data)
