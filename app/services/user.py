from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import UserOrganizationRole, UserRole, UserStatus
from app.repositories import userRepository
from app.schemas import User, UserCreate, UserInvite, UserUpdate, UserUpdateStatus


class UserService:
    """User Service class"""

    async def me(self, session: AsyncSession, email: str) -> User:
        """
        returns the current user for the given email, if not found user
        a new one will be created with default profile with 'OWNER' role
        """

        user = await userRepository.find_by_email(session, email)

        if not user:
            name = email.split("@")[0]
            owner_user = UserCreate(
                email=email, name=name, role=UserRole.OWNER, status=UserStatus.ACTIVE
            )
            return await userRepository.create_with_default_profile(
                session, obj_in=owner_user
            )

        if user.status == UserStatus.INVITED:
            update_status = UserUpdateStatus(status=UserStatus.ACTIVE)
            await userRepository.update(session, uuid=user.uuid, obj_in=update_status)

        return user

    async def invite_user(self, session: AsyncSession, user_in: UserInvite):
        """Creates a new user with status `INVITED` and default profile"""

        if user_in.role not in UserOrganizationRole:
            raise ValueError(f"Cannot invite user with role: {user_in.role}")

        name = user_in.email.split("@")[0]
        invited_user = UserCreate(
            email=user_in.email,
            role=UserRole(user_in.role.value),
            name=name,
            status=UserStatus.INVITED,
        )
        return await userRepository.create_with_default_profile(
            session, obj_in=invited_user
        )

    async def all_users(
        self,
        session: AsyncSession,
        filters: dict,
        skip: int = 0,
        limit: int = 100,
    ):
        """Returns list of users"""
        return await userRepository.search(
            session, skip=skip, limit=limit, filters=filters
        )

    async def get_user(self, session: AsyncSession, user_id: UUID):
        """Returns user details"""
        return await userRepository.find_by_id(session, user_id)

    async def update_user(
        self, session: AsyncSession, user_id: UUID, user_in: UserUpdate
    ):
        """Update user"""

        if user_in.role not in UserOrganizationRole:
            raise ValueError(f"Cannot update user with role: {user_in.role}")

        # FIXME: UserRole and UserOrganizationRole
        return await userRepository.update(session, uuid=user_id, obj_in=user_in)

    async def delete_user(self, session: AsyncSession, user_id: UUID):
        """delete user"""

        user = await userRepository.find_by_id(session, uuid=user_id)

        if user.role not in UserOrganizationRole:
            raise ValueError(f"Cannot delete user with role: {user.role}")

        return await userRepository.delete(session, uuid=user_id)


userService = UserService()
