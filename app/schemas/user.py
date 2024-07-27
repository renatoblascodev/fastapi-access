from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums import UserOrganizationRole, UserRole, UserStatus


class UserBase(BaseModel):
    """Shared properties"""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(max_length=60)
    name: str = Field(max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole
    status: UserStatus


class UserPreferences(BaseModel):
    """Shared properties"""

    model_config = ConfigDict(from_attributes=True)

    language: str = Field(max_length=14)
    notification: bool


class TermsOfUse(BaseModel):
    """Shared properties"""

    model_config = ConfigDict(from_attributes=True)

    agreement: bool


class UserProfile(BaseModel):
    """Shared properties"""

    model_config = ConfigDict(from_attributes=True)

    user_preferences: UserPreferences
    terms_of_use: TermsOfUse


class User(UserBase):
    """Properties to return user details"""

    uuid: UUID
    created_at: Optional[datetime] = None


class UserMe(User):
    """Properties to return current user details"""

    user_profile: UserProfile


class UserInvite(BaseModel):
    """Properties to receive via API on invite user"""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    role: UserOrganizationRole


class UserCreate(UserBase):
    """Properties to receive via API on creation"""


class UserUpdate(BaseModel):
    """Properties to receive via API on update"""

    model_config = ConfigDict(from_attributes=True)

    name: str
    phone: Optional[str] = None
    role: UserOrganizationRole
    status: UserStatus


class UserUpdateStatus(BaseModel):
    """Properties to update user status"""

    model_config = ConfigDict(from_attributes=True)

    status: UserStatus
