from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from typing import Optional

from src.auth.repository.db_connection import get_db_session
from src.auth.services import UserServiceFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):  # Modelo do usuário
    name: str
    user_name: str
    code: str


def get_current_user(token: str = Depends(oauth2_scheme), db_session=Depends(get_db_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        authentication_service = UserServiceFactory.create_authentication_user_service(db_session)
        user = authentication_service.get_user_from_token(token)
        token_data = User(**user.model_dump())
    except JWTError:
        raise credentials_exception
    return token_data
