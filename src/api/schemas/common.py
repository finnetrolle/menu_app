"""
Common API response schemas and error handling.
Provides standardized response formats across all endpoints.
"""

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel):
    """Generic success response."""
    status: str = "success"
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response with details."""
    status: str = "error"
    error: str
    detail: Optional[str] = None


class DataResponse(BaseModel, Generic[T]):
    """Generic response wrapper for single items."""
    status: str = "success"
    data: T


class ListResponse(BaseModel, Generic[T]):
    """Generic response wrapper for lists with pagination."""
    status: str = "success"
    data: List[T]
    total: int
    skip: int = 0
    limit: int = 100


class PaginatedRequest(BaseModel):
    """Base class for paginated requests."""
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(20, ge=1, le=100, description="Maximum number of records to return")


# Exception classes for API errors
class APIError(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, status_code: int = 400, detail: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class NotFoundError(APIError):
    """Resource not found error."""
    
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with id '{identifier}' not found"
        super().__init__(message, status_code=404)


class ValidationError(APIError):
    """Validation error."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status_code=422, detail=detail)


class ConflictError(APIError):
    """Conflict error (e.g., duplicate resource)."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status_code=409, detail=detail)


class BadRequestError(APIError):
    """Bad request error."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status_code=400, detail=detail)
