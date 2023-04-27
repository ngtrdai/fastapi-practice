from sqlalchemy import Boolean, Column, String, Uuid, ForeignKey
from database import Base
from schemas.base_entity import BaseEntity
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base, BaseEntity):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String(128), nullable=False)
    company_id = Column(Uuid, ForeignKey('companies.id'), nullable=False)

    company = relationship("Company")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, self) -> bool:
    return pwd_context.verify(password, self.hashed_password)