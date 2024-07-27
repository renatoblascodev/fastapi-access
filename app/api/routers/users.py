from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from typing_extensions import Annotated

from app.api.dependencies.core import DBSessionDep
from app.exceptions import EntityNotFound, IntegrityConstraintViolation
from app.schemas import PaginatedResponse, User, UserInvite, UserMe, UserUpdate
from app.services import userService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=UserMe)
async def me(db_session: DBSessionDep, email: str):
    """Returns logged user"""
    return await userService.me(db_session, email)


@router.post("/invite", response_model=User)
async def invite_user(db_session: DBSessionDep, user_in: UserInvite):
    """Invite a new user"""

    try:
        return await userService.invite_user(db_session, user_in=user_in)
    except IntegrityConstraintViolation as ex:
        raise HTTPException(
            status_code=400, detail="Integrity constraint violated"
        ) from ex
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex)) from ex


@router.get("/", response_model=PaginatedResponse[User])
async def all_users(
    db_session: DBSessionDep,
    name: Optional[str] = None,
    page: Annotated[int, Query(gt=0)] = 1,
    size: Annotated[int, Query(gt=0)] = 100,
):
    """Returns list of users"""

    skip = (page - 1) * size

    filters = {"name": name}

    users, total = await userService.all_users(
        db_session, filters, skip=skip, limit=size
    )

    return {
        "page": page,
        "size": size,
        "count": len(users),
        "total": total,
        "items": users,
    }


@router.get("/{user_id}", response_model=User)
async def user_details(
    user_id: UUID,
    db_session: DBSessionDep,
):
    """Returns user details"""
    try:
        return await userService.get_user(db_session, user_id)
    except EntityNotFound as ex:
        raise HTTPException(status_code=404, detail="User not found") from ex


@router.put("/{user_id}", response_model=User)
async def update_user(db_session: DBSessionDep, user_id: UUID, user_in: UserUpdate):
    """Update user"""

    try:
        return await userService.update_user(
            db_session, user_id=user_id, user_in=user_in
        )
    except EntityNotFound as ex:
        raise HTTPException(status_code=404, detail="User not found") from ex
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex)) from ex


@router.delete("/{user_id}", response_model=User)
async def delete_user(db_session: DBSessionDep, user_id: UUID):
    """delete user"""

    try:
        return await userService.delete_user(db_session, user_id=user_id)
    except EntityNotFound as ex:
        raise HTTPException(status_code=404, detail="User not found") from ex
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex)) from ex
