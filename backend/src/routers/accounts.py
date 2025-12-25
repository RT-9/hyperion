from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..core.database import get_db
from ..services.accounts import AccountService
from ..schemas.accounts import UserCreate, UserResponse, UserLogin
from ..core.exc import DuplicateEntryError, InvalidPasswordError, Unauthorised

account_router = APIRouter(prefix="/api", tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/accounts/login")

@account_router.post("/accounts", response_model=UserResponse)
async def post_create_account(account: UserCreate, session=Depends(get_db)):
    user_service = AccountService(session)
    try:
        user = await user_service.create_user(account)
    except DuplicateEntryError as e:
        raise HTTPException(409, detail=str(e))
    except InvalidPasswordError as e:
        raise HTTPException(422, detail=str(e))
    except Exception:
        raise HTTPException(500)

    return user


@account_router.post("/accounts/login")
async def post_login(
    form: OAuth2PasswordRequestForm = Depends(),
    session = Depends(get_db)
):
    """
    Authenticate a user using a JSON body and return a JWT.

    :param login_data: The credentials provided as JSON.
    :type login_data: UserLogin
    :param session: The asynchronous database session.
    :type session: AsyncSession
    :raises Unauthorised: If the credentials are invalid.
    :return: The access token and its type.
    :rtype: dict
    """
    user_service = AccountService(session)
    login_data = UserLogin(username=form.username, password=form.password)
    try:
        access_token = await user_service.authorise_user(login_data)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Unauthorised as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(500)
