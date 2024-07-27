import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import EntityNotFound
from app.repositories import organizationRepository, userRepository
from app.schemas import OrganizationCreate

logger = logging.getLogger(__name__)


class OrganizationService:
    """User Service class"""

    async def initial_setup(
        self, session: AsyncSession, user_email: str, org_in: OrganizationCreate
    ):
        """Creates a new organization with defaults and add to current user"""

        user = await userRepository.find_by_email(session, user_email)

        if not user:
            logger.error("No User found with email: %s", user_email)
            raise EntityNotFound

        organization = await organizationRepository.create_with_default_config(
            session, obj_in=org_in
        )

        await userRepository.add_user_to_organization(
            session, user=user, organization=organization
        )

        return organization

    async def my_organizations(self, session: AsyncSession, user_email: str):
        """Returns list of organizations by user"""
        return await userRepository.all_user_organizations(session, email=user_email)


organizationService = OrganizationService()
