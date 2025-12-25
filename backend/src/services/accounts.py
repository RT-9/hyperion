import re
from datetime import datetime, timedelta, timezone
from jwt import encode
from pwdlib import PasswordHash
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import settings
from ..core.exc import DuplicateEntryError, InvalidPasswordError, Unauthorised
from ..models.accounts import Accounts
from ..schemas.accounts import UserCreate, UserGet, UserLogin

# Password policy: 8-64 chars, at least one uppercase, one lowercase, one digit, and one special char.
PATTERN = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,64}$'
)


class AccountService:
    """
    Service layer for managing user accounts, handling secure password hashing 
    via pwdlib and JWT-based authorisation.
    """

    
    password_hash_helper = PasswordHash.recommended(
    )

    def __init__(self, session: AsyncSession):
        """
        Initialise the AccountService with a database session.

        :param session: The asynchronous database session.
        :type session: AsyncSession
        """
        self.db = session

    async def get_user(self, user: UserGet) -> Accounts | None:
        """
        Retrieve a user instance based on ID or username.

        :param user: The criteria to search for the user.
        :type user: UserGet
        :raises ValueError: If neither ID nor username is provided.
        :return: The account instance or None if not found.
        :rtype: Accounts | None
        """
        if user.id:
            qry = select(Accounts).where(Accounts.id == user.id)
        elif user.username:
            qry = select(Accounts).where(
                Accounts.username == user.username.lower())
        else:
            raise ValueError("Either id or username must be specified")

        result = await self.db.execute(qry)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate) -> Accounts:
        """
        Register a new user and store their hashed password.

        :param user: The user registration data.
        :type user: UserCreate
        :raises InvalidPasswordError: If the password policy or confirmation fails.
        :raises DuplicateEntryError: If the username already exists.
        :return: The newly created account instance.
        :rtype: Accounts
        """
        if not user.password == user.password_confirm:
            raise InvalidPasswordError(
                "Password and password_confirm did not match.")

        account = Accounts(
            username=user.username.lower(),
            password=self.password_hash(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
        )

        try:
            self.db.add(account)
            await self.db.commit()
            await self.db.refresh(account)
        except IntegrityError:
            await self.db.rollback()
            raise DuplicateEntryError("User already exists")

        return account

    async def authorise_user(self, user: UserLogin) -> str:
        """
        Verify credentials and return a JWT. Updates the hash if security 
        parameters are outdated.

        :param user: The login credentials.
        :type user: UserLogin
        :raises Unauthorised: If verification fails.
        :return: An encoded JWT string.
        :rtype: str
        """
        qry = select(Accounts).where(
            Accounts.username == user.username.lower())
        res = await self.db.execute(qry)
        account = res.scalar_one_or_none()

        if not account:
            raise Unauthorised("Username or Password is incorrect.")

        # verify_and_update returns a result object (verified: bool, updated_hash: str | None)
        verified,  updated_hash = self.password_hash_helper.verify_and_update(
            user.password, account.password
        )

        if not verified:
            raise Unauthorised("Username or Password is incorrect.")

        # If a re-hash is recommended by pwdlib, we update it in the database.
        if updated_hash:
            update_qry = (
                update(Accounts)
                .where(Accounts.id == account.id)
                .values(password=updated_hash)
            )
            await self.db.execute(update_qry)
            await self.db.commit()

        return self.encode_jwt(sub=account.id)

    def password_hash(self, password) -> str:
        """
        Validate a password against the policy and return a secure hash.

        :param password: The plain-text password.
        :type password: str
        :raises InvalidPasswordError: If the password policy is not met.
        :return: The secure password hash.
        :rtype: str
        """
        if PATTERN.match(password):
            return self.password_hash_helper.hash(password)
        raise InvalidPasswordError("Password did not meet password policy.")

    @staticmethod
    def encode_jwt(sub) -> str:
        """
        Generate a JWT for the given subject.

        :param sub: The subject of the token (user ID).
        :type sub: str | int
        :return: The encoded JWT.
        :rtype: str
        """
        now = datetime.now(tz=timezone.utc)
        payload = {
            "iss": "hyperion_backend",
            "nbf": now - timedelta(seconds=3),
            "exp": now + timedelta(minutes=15, seconds=3),
            "iat": now,
            "sub": str(sub),
        }
        return encode(
            payload,
            key=settings.JWT_SECRET,
            algorithm="HS512",
            sort_headers=True
        )
