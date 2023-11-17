from fastapi import HTTPException, status, APIRouter, Depends
from pydantic import BaseModel

from src.auth.domain.models import UserModel
from src.auth.domain.user_erros import UsernameAlreadyRegistered
from src.auth.repository.db_connection import get_db_session
from src.auth.services import UserServiceFactory

router = APIRouter()


class NewUserInput(BaseModel):
    name: str
    user_name: str
    password: str


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
        user_service = UserServiceFactory.create_investment_service(db_session)
        user_model = UserModel(code=None, created_at=None, **new_user_form_data.model_dump())
        created_user = user_service.create(user_model)
        return UserResponse(**created_user.model_dump())

    except UsernameAlreadyRegistered as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to retrieve investments.")
