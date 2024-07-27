from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums import OrganizationStatus


class OrganizationBase(BaseModel):
    """Shared properties"""

    model_config = ConfigDict(from_attributes=True)

    cnpj: str = Field(max_length=20)
    email: EmailStr = Field(max_length=60)
    name: str = Field(max_length=50)
    description: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    status: OrganizationStatus = OrganizationStatus.ACTIVE


class Organization(OrganizationBase):
    """Properties to return organization details"""

    uuid: UUID
    created_at: Optional[datetime] = None


class OrganizationAddress(BaseModel):
    """Properties to return organization address"""

    model_config = ConfigDict(from_attributes=True)

    address: str = Field(max_length=100)
    city: str = Field(max_length=50)
    state: str = Field(max_length=2)
    postal_code: str = Field(max_length=20)


class OrganizationCreate(OrganizationBase):
    """Properties to receive via API on creation"""

    address: OrganizationAddress
