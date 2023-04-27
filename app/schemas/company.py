from sqlalchemy import Column, String, Enum, Numeric, DateTime
from database import Base
from schemas.base_entity import BaseEntity
import enum

class CompanyMode(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String(50), nullable=False)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False,
                  default=CompanyMode.ACTIVE)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)