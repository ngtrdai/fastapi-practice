from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserModel(BaseModel):
    username: Field(str, min_length=3, max_length=50)
    email: Field(str, min_length=3, max_length=128)
    first_name: Field(str, min_length=3, max_length=50)
    last_name: Field(str, min_length=3, max_length=50)
    hashed_password: Field(str, min_length=3, max_length=128)
    is_active: Field(bool, default=True)
    is_admin: Field(bool, default=False)

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    company_id: UUID or None
    is_active: bool or None
    is_admin: bool or None