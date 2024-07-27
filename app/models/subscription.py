import uuid as puuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import BaseModel
from app.enums import PaymentMethod, PaymentStatus, VoucherStatus

from .service_plan import ServicePlan


class Subscription(BaseModel):
    """Subscription model"""

    __tablename__ = "subscription"

    service_plan_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("service_plan.uuid")
    )
    service_plan: Mapped["ServicePlan"] = relationship()

    organization_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("organization.uuid")
    )

    payment: Mapped["Payment"] = relationship()


class Payment(BaseModel):
    """Payment model"""

    __tablename__ = "payment"

    method: Mapped[PaymentMethod] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(nullable=False)

    subscription_uuid: Mapped[puuid.UUID] = mapped_column(
        ForeignKey("subscription.uuid")
    )

    __table_args__ = (UniqueConstraint("subscription_uuid"),)


class Voucher(BaseModel):
    """Voucher model"""

    __tablename__ = "voucher"

    code: Mapped[str] = mapped_column(
        String(30), index=True, unique=True, nullable=False
    )
    status: Mapped[VoucherStatus] = mapped_column(
        nullable=False, default=VoucherStatus.ACTIVE
    )
