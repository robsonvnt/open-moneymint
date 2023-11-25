from _datetime import timedelta
from fastapi import HTTPException, status, APIRouter, Depends
from pydantic import BaseModel

from auth.domain.models import UserModel
from auth.domain.user_erros import UsernameAlreadyRegistered, UserNotFound
from auth.repository.db_connection import get_db_session
from auth.service.services import UserServiceFactory
from auth.user import User, get_current_user

router = APIRouter()


class NewUserInput(BaseModel):
    name: str
    user_name: str
    password: str


class LoginInput(BaseModel):
    user_name: str
    password: str


class AccessTokenResponse(BaseModel):
    access_token: str


class UserResponse(BaseModel):
    code: str
    name: str
    user_name: str


@router.post("/users/signup", response_model=UserResponse)
async def signup(
        new_user_form_data: NewUserInput,
        db_session=Depends(get_db_session)
):
    try:
        user_service = UserServiceFactory.create_user_service(db_session)
        user_model = UserModel(code=None, created_at=None, **new_user_form_data.model_dump())
        created_user = user_service.create(user_model)
        return UserResponse(**created_user.model_dump())

    except UsernameAlreadyRegistered as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to retrieve user.")


@router.post("/users/signin", response_model=AccessTokenResponse)
async def signin(
        login_data: LoginInput,
        db_session=Depends(get_db_session)
):
    try:
        authentication_user_service = UserServiceFactory.create_authentication_user_service(db_session)
        user = authentication_user_service.authenticate_user(login_data.user_name, login_data.password)
        token = authentication_user_service.create_access_token(user, timedelta(days=1))
        return AccessTokenResponse(access_token=token)

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to retrieve user.")



@router.get("/users/me", response_model=UserResponse)
async def get_me(
        current_user: User = Depends(get_current_user)
):
    return UserResponse(**current_user.model_dump())