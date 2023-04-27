from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db_context
from services.auth import authService
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_context)):
    user = authService.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise authService.token_exception()
    
    access_token_expires = timedelta(minutes=authService.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": authService.create_access_token(user, expires=access_token_expires),
        "token_type": "bearer"
    }