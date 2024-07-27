import uuid as puuid
from datetime import datetime

from sqlalchemy import types
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class BaseModel(Base):
    """Declarative base class"""

    __name__: str
    __abstract__ = True

    uuid: Mapped[puuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        default=lambda: str(puuid.uuid4()),
        unique=True,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"{type(self).__name__}[{self.uuid}]"
