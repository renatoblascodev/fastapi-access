import logging
from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions import IntegrityConstraintViolation
from app.models import Organization, TermsOfUse
from app.models import User as UserModel
from app.models import UserPreferences, UserProfile
from app.schemas import User, UserCreate

from .base import RepositoryCreate, RepositoryDelete, RepositoryRead, RepositoryUpdate

logger = logging.getLogger(__name__)


class UserRepository(
    RepositoryRead, RepositoryCreate, RepositoryUpdate, RepositoryDelete
):
    """User Repository class"""

    async def find_by_email(self, session: AsyncSession, email: str):
        """returns the user for the given email otherwise ´None´"""
        return (
            await session.scalars(
                select(UserModel)
                .options(selectinload(UserModel.user_profile))
                .where(UserModel.email == email)
            )
        ).first()

    async def create_with_default_profile(
        self, session: AsyncSession, *, obj_in: UserCreate
    ) -> UserModel:
        """Creates new user with default profile"""
        try:
            user = UserModel(**obj_in.model_dump())
            profile = UserProfile()
            profile.terms_of_use = TermsOfUse()
            profile.user_preferences = UserPreferences()
            user.user_profile = profile
            profile.user = user

            session.add(user)
            session.add(profile)
            await session.commit()
            await session.refresh(user)
            await session.refresh(user, ["user_profile"])

            return user
        except IntegrityError as e:
            logger.error("Integrity constraint violeted: %s", exc_info=1)
            raise IntegrityConstraintViolation from e

    async def add_user_to_organization(
        self, session: AsyncSession, *, user: UserModel, organization: Organization
    ):
        """add user to organization"""

        await session.refresh(user, ["organizations"])
        user.organizations.append(organization)

        session.add(user)
        await session.commit()

        await session.refresh(user)
        await session.refresh(organization)

    async def search(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100, filters: dict
    ) -> Tuple[List[User], int]:
        """Returns all items filtered and limited by `skip` and `limt` params"""

        db_filters = []

        for key, value in filters.items():
            if value is not None:
                db_filters.append(getattr(self.model, key).ilike(f"%{value}%"))

        query = select(self.model).filter(*db_filters)

        result = await session.scalars(
            query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        )
        # pylint: disable-next=not-callable
        total = await session.scalar(select(func.count()).select_from(query.subquery()))

        return (result.all(), total)

    async def all_user_organizations(
        self, session: AsyncSession, *, email: str
    ) -> List[Organization]:
        """Returns all user organizations"""

        user = (
            await session.scalars(
                select(UserModel)
                .options(selectinload(UserModel.organizations))
                .where(UserModel.email == email)
            )
        ).one()

        return user.organizations


userRepository = UserRepository(UserModel)
