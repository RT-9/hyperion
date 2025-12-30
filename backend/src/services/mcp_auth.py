import uuid
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from mcp.server.auth.provider import AccessToken, TokenVerifier

from ..models.accounts import MCPToken
from ..schemas.accounts import MCPTokenResponse
from ..core.exc import DuplicateEntryError
from ..core.database import async_session_factory
class MCPAuthService:
    
    def __init__(self, session:AsyncSession):
        self.db = session 
    
    
    async def create_mcp_token(self, user_id):
        try:
            token_expiration_time = datetime.now(tz=timezone.utc) + timedelta(days=30, seconds=3)
            token = secrets.token_hex(64)
            token_hash = hashlib.sha3_512(token.encode()).hexdigest()
            new_token = MCPToken(
                account_id=user_id,
                token=token_hash,
                expires_at=token_expiration_time
                
            )
            self.db.add(new_token)
            await self.db.commit()
            await self.db.refresh(new_token)
            return MCPTokenResponse(token=token, exp=token_expiration_time)
        except IntegrityError:
            await self.db.rollback()
            raise DuplicateEntryError("Duplicate MCP token.")

        
    async def get_mcp_tokens(self, user_id):
        try:
            qry = select(MCPToken).where(MCPToken.account_id==user_id)
            tokens = await self.db.execute(qry)
            return tokens.all()
        except IntegrityError:
            await self.db.rollback()
            raise RuntimeError("Something went wrong.")

class MCPAuthToken(TokenVerifier):
    
    async def verify_token(self, token: str) -> AccessToken | None:
        async with async_session_factory() as db:
            now = datetime.now(tz=timezone.utc)
            token_hash = hashlib.sha3_512(token.encode()).hexdigest()
            qry = select(MCPToken).where(MCPToken.token == token_hash).where(MCPToken.expires_at > now)
            db_token = await db.execute(qry)
            db_token = db_token.scalar_one_or_none()
            if not db_token:
                return None
            return AccessToken(token=token,client_id=str(db_token.account_id), expires_at=db_token.expires_at, scopes=["all"])
            
        
    