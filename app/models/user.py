import uuid as puuid
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import Base, BaseModel
from app.enums import UserRole, UserStatus

from . import organization

user_organization_table = Table(
    "user_organization",
    Base.metadata,
    Column("user_uuid", ForeignKey("user.uuid"), primary_key=True),
    Column("organization_uuid", ForeignKey("organization.uuid"), primary_key=True),
)


class User(BaseModel):
    """User model"""

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(60), index=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(nullable=False)
    status: Mapped[UserStatus] = mapped_column(nullable=False)

    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    organizations: Mapped[List[organization.Organization]] = relationship(
        secondary=user_organization_table
    )


class UserProfile(BaseModel):
    """User Profile model"""

    __tablename__ = "user_profile"

    terms_of_use: Mapped["TermsOfUse"] = relationship(
        back_populates="user_profile",
        lazy="joined",
        innerjoin=True,
        cascade="all, delete-orphan",
    )
    user_preferences: Mapped["UserPreferences"] = relationship(
        back_populates="user_profile",
        lazy="joined",
        innerjoin=True,
        cascade="all, delete-orphan",
    )

    user_uuid: Mapped[puuid.UUID] = mapped_column(ForeignKey("user.uuid"))
    user: Mapped["User"] = relationship(
        back_populates="user_profile", single_parent=True
    )

    __table_args__ = (UniqueConstraint("user_uuid"),)


class UserPreferences(BaseModel):
    """User Preferences model"""

    __tablename__ = "user_preferences"

    language: Mapped[str] = mapped_column(String(14), nullable=False, default="pt-BR")
    notification: Mapped[bool] = mapped_column(nullable=False, default=True)

    user_profile_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("user_profile.uuid")
    )
    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="user_preferences", single_parent=True
    )

    __table_args__ = (UniqueConstraint("user_profile_uuid"),)


class TermsOfUse(BaseModel):
    """Terms of User model"""

    __tablename__ = "terms_of_use"

    agreement: Mapped[bool] = mapped_column(nullable=False, default=False)

    user_profile_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("user_profile.uuid")
    )
    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="terms_of_use", single_parent=True
    )
    tou_versions: Mapped[List["TOUVersion"]] = relationship()

    __table_args__ = (UniqueConstraint("user_profile_uuid"),)


class TOUVersion(BaseModel):
    """TOU Version model"""

    __tablename__ = "tou_version"

    version: Mapped[str] = mapped_column(String(20), nullable=False)
    document_uri: Mapped[str] = mapped_column(nullable=False)

    tou_uuid: Mapped[puuid.UUID] = mapped_column(ForeignKey("terms_of_use.uuid"))
