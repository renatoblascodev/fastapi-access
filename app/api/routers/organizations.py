from typing import List

from fastapi import APIRouter, HTTPException, Query
from typing_extensions import Annotated

from app.api.dependencies.core import DBSessionDep
from app.exceptions import IntegrityConstraintViolation
from app.schemas import ListResponse, Organization, OrganizationCreate
from app.services import organizationService

router = APIRouter(prefix="/organizations", tags=["Organization"])


@router.post("/setup", response_model=Organization)
async def create_initial_organization(
    db_session: DBSessionDep,
    user_email: Annotated[str, Query()],
    org_in: OrganizationCreate,
):
    """Create a new organization for current user"""

    try:
        return await organizationService.initial_setup(
            db_session, user_email=user_email, org_in=org_in
        )
    except IntegrityConstraintViolation as ex:
        raise HTTPException(
            status_code=400, detail="Integrity constraint violated"
        ) from ex
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex)) from ex


@router.get("/my-orgs", response_model=ListResponse[Organization])
async def my_organizations(db_session: DBSessionDep, email: str):
    """Returns organizations for logged user"""

    organizatios = await organizationService.my_organizations(db_session, email)

    return {
        "items": organizatios,
    }
