from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    code: Optional[str]
    name: str
    user_name: str
    password: str
    created_at: Optional[date]
