from fastapi import WebSocket, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib
from datetime import datetime, timezone
from typing import Optional

# Deine Imports
from ..models.accounts import ClientTokens, HyperionClients
from .database import get_db


async def get_current_device(
    websocket: WebSocket, token: str = Query(...), db: AsyncSession = Depends(get_db)
) -> HyperionClients:
    """
    Authenticate a WebSocket connection using a query token.

    This dependency verifies the token hash against the database, checks for
    expiration, and retrieves the associated client. If authentication fails,
    the WebSocket is closed with a policy violation code.

    :param websocket: The active WebSocket connection.
    :type websocket: WebSocket
    :param token: The plain-text authentication token passed via query params.
    :type token: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The authenticated client instance.
    :rtype: HyperionClients
    :raises WebSocketException: If the token is invalid or expired.
    """

    token_hash = hashlib.sha3_512(token.encode()).hexdigest()

    stmt = (
        select(ClientTokens, HyperionClients)
        .join(HyperionClients, ClientTokens.client_id == HyperionClients.id)
        .where(ClientTokens.token_hash == token_hash)
    )

    result = await db.execute(stmt)
    row = result.first()

    if not row:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    token_record, client = row

    now = datetime.now(timezone.utc)

    expires_at = token_record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return client
