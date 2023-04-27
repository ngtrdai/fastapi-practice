from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import User
from database import get_db_context
from services.auth import authService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_users(db: Session = Depends(get_db_context), current_user: User = Depends(authService.token_interceptor)):
    return db.query(User).all()
