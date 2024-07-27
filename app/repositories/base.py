import logging
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base_class import BaseModel as Base
from app.exceptions import EntityNotFound, IntegrityConstraintViolation

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)  # ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository for Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `model`: A SQLAlchemy model class
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model


class RepositoryRead(RepositoryBase):
    """Read Respository"""

    async def find_by_id(
        self, session: AsyncSession, uuid: UUID
    ) -> Optional[ModelType]:
        """Return item by uuid"""
        try:
            result = await session.scalars(
                select(self.model).where(self.model.uuid == uuid)
            )
            return result.one()
        except NoResultFound as e:
            logger.error("No %s found for uuid: %s", self.model.__name__, uuid)
            raise EntityNotFound from e

    async def find_all(self, session: AsyncSession, *, skip: int = 0, limit: int = 100):
        """Returns all items limited by `skip` and `limt` params"""
        result = await session.scalars(
            select(self.model)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.all()


class RepositoryCreate(RepositoryBase):
    """Create Repository"""

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        """Creates new item"""
        try:
            new_obj = self.model(**obj_in.model_dump())
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            logger.info("%s successfull created", self.model.__name__)
            return new_obj
        except IntegrityError as e:
            logger.error("Integrity constraint violeted: %s", exc_info=1)
            raise IntegrityConstraintViolation from e


class RepositoryUpdate(RepositoryBase):
    """Update Repository"""

    async def update(
        self, session: AsyncSession, *, uuid: UUID, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update item"""
        entity = (
            await session.scalars(select(self.model).where(self.model.uuid == uuid))
        ).first()

        if not entity:
            logger.error("No %s found for uuid: %s", self.model.__name__, uuid)
            raise EntityNotFound

        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)

        await session.commit()
        await session.refresh(entity)
        logger.info("%s successfull updated", self.model.__name__)
        return entity


class RepositoryDelete(RepositoryBase):
    """Delete Repository"""

    async def delete(self, session: AsyncSession, *, uuid: UUID) -> ModelType:
        """Remove item by id"""
        entity = (
            await session.scalars(select(self.model).where(self.model.uuid == uuid))
        ).first()

        if not entity:
            logger.error("No %s found for uuid: %s", self.model.__name__, uuid)
            raise EntityNotFound

        await session.delete(entity)
        await session.commit()
        logger.info("%s successfull deleted", self.model.__name__)
        return entity
