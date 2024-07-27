import uuid as puuid
from typing import List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import BaseModel
from app.enums import OrganizationProvider, OrganizationStatus

from .subscription import Subscription


class Organization(BaseModel):
    """Organization model"""

    __tablename__ = "organization"

    cnpj: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[OrganizationStatus] = mapped_column(nullable=False)

    address: Mapped["OrganizationAddress"] = relationship(lazy="joined", innerjoin=True)
    organization_config: Mapped["OrganizationConfig"] = relationship(
        back_populates="organization"
    )
    subscriptions: Mapped[List["Subscription"]] = relationship()


class OrganizationAddress(BaseModel):
    """Organization Address model"""

    __tablename__ = "organization_address"

    address: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)

    organization_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("organization.uuid")
    )

    __table_args__ = (UniqueConstraint("organization_uuid"),)


class OrganizationConfig(BaseModel):
    """Organization Config model"""

    __tablename__ = "organization_config"

    snow_company: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    customer_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    ch_client_id: Mapped[str] = mapped_column(String(20), nullable=False)
    security_group: Mapped[str] = mapped_column(nullable=True)

    organization_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("organization.uuid")
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="organization_config", single_parent=True
    )
    org_config_providers: Mapped[List["OrgConfigProvider"]] = relationship(
        lazy="selectin"
    )

    __table_args__ = (UniqueConstraint("organization_uuid"),)


class OrgConfigProvider(BaseModel):
    """Organization Config Provider model"""

    __tablename__ = "org_config_provider"

    provider: Mapped[OrganizationProvider] = mapped_column(nullable=False)
    account_id: Mapped[str] = mapped_column(String(20), nullable=True)
    account_regions: Mapped[str] = mapped_column(nullable=True)
    project_id: Mapped[str] = mapped_column(String(40), nullable=True)
    project_zones: Mapped[str] = mapped_column(nullable=True)
    subscription_id: Mapped[str] = mapped_column(String(20), nullable=True)
    subscription_dn: Mapped[str] = mapped_column(nullable=True)
    subscription_tenant: Mapped[str] = mapped_column(String(20), nullable=True)

    organization_config_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("organization_config.uuid")
    )
