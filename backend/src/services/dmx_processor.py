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

import asyncio
import logging

import redis.asyncio as redis
from fastapi import WebSocket

from .dmx_protocol import DMXProtocol

logger = logging.getLogger("hyperion")


class DMXProcessor:
    """
    Handles DMX signal processing and WebSocket communication.
    """

    def __init__(self, websocket: WebSocket, redis_client: redis.Redis):
        """
        Initialise the processor with a WebSocket and a Redis client.

        :param websocket: The active WebSocket connection.
        :param redis_client: The Redis client instance for Pub/Sub.
        """
        self.ws = websocket
        self.redis = redis_client
        self.channel_name = "hyperion:dmx:global"

    async def json_data(self, data):
        """
        Handle incoming JSON data from the DMX node (Client -> Server).

        :param data: The JSON payload received.
        """
        print(f"Received from Node: {data}")

        await self.ws.send_text("ACK_FROM_SERVER")

    async def subscribe_and_stream(self):
        """
        Subscribe to the Redis channel and stream data to the WebSocket.

        This runs in an infinite loop and forwards any message published
        to 'hyperion:dmx:global' directly to the connected DMX node.
        (Server/Redis -> Client)
        """
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.channel_name)

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    b64_payload = message["data"]

                    raw_bytes = DMXProtocol.from_transport(b64_payload)

                    await self.ws.send_bytes(raw_bytes)
        except Exception as e:
            logger.error(f"Redis Subscription Error: {e}")
        finally:
            await pubsub.unsubscribe(self.channel_name)
