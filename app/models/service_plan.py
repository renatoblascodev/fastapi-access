import uuid as puuid
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import Base, BaseModel

product_plan_table = Table(
    "product_service_plan",
    Base.metadata,
    Column("product_uuid", ForeignKey("product.uuid"), primary_key=True),
    Column("service_plan_uuid", ForeignKey("service_plan.uuid"), primary_key=True),
)


class Product(BaseModel):
    """Product model"""

    __tablename__ = "product"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)


class ServicePlan(BaseModel):
    """Service Plan model"""

    __tablename__ = "service_plan"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    trial: Mapped[bool] = mapped_column(nullable=False, default=False)
    trial_days: Mapped[int] = mapped_column(nullable=True, default=0)

    contract_uuid: Mapped[puuid.UUID] = mapped_column(ForeignKey("contract.uuid"))
    contract: Mapped["Contract"] = relationship()
    products: Mapped[List[Product]] = relationship(secondary=product_plan_table)


class Contract(BaseModel):
    """Contract model"""

    __tablename__ = "contract"

    version: Mapped[str] = mapped_column(String(20), nullable=False)
    document_uri: Mapped[str] = mapped_column(nullable=False)
