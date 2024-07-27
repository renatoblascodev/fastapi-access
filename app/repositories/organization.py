import logging
import random
import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import IntegrityConstraintViolation
from app.models import Organization as OrganizationModel
from app.models import OrganizationAddress, OrganizationConfig
from app.schemas import OrganizationCreate

from .base import RepositoryRead

logger = logging.getLogger(__name__)


class OrganizationRepository(RepositoryRead):
    """User Repository class"""

    async def create_with_default_config(
        self, session: AsyncSession, *, obj_in: OrganizationCreate
    ) -> OrganizationModel:
        """Creates new organization with default config"""

        try:
            organization = OrganizationModel(**obj_in.model_dump(exclude=["address"]))
            address = OrganizationAddress(**obj_in.address.model_dump())

            config = OrganizationConfig()
            config.snow_company = "".join(random.choices(string.ascii_lowercase, k=20))
            config.customer_code = "".join(random.choices(string.ascii_lowercase, k=20))
            config.ch_client_id = "C123"

            organization.address = address
            organization.organization_config = config

            session.add(organization)
            session.add(address)
            session.add(config)
            await session.commit()
            await session.refresh(organization)

            return organization
        except IntegrityError as e:
            logger.error("Integrity constraint violeted: %s", exc_info=1)
            raise IntegrityConstraintViolation from e


organizationRepository = OrganizationRepository(OrganizationModel)
