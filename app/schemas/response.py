from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response"""

    page: int = Field(description="Page number")
    size: int = Field(description="Number of items per page")
    count: int = Field(description="Number of items returned in the response")
    total: int = Field(description="Total of items")
    items: List[T] = Field(description="List of items returned")


class ListResponse(BaseModel, Generic[T]):
    """List response"""

    items: List[T] = Field(description="List of items returned")
