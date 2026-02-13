"""
Error handling middleware and exception handlers.
Provides centralized error handling for the API.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.api.schemas.common import APIError, ErrorResponse


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handler for custom API errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            error=exc.message,
            detail=exc.detail
        ).model_dump()
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status="error",
            error="Validation failed",
            detail="; ".join(errors)
        ).model_dump()
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handler for database integrity errors (e.g., unique constraint violations)."""
    error_msg = str(exc.orig) if exc.orig else str(exc)
    
    # Parse common SQLite/PostgreSQL constraint errors
    if "UNIQUE constraint failed" in error_msg or "duplicate key" in error_msg.lower():
        detail = "Resource already exists"
    elif "FOREIGN KEY constraint failed" in error_msg or "foreign key" in error_msg.lower():
        detail = "Referenced resource not found"
    else:
        detail = "Database constraint violation"
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            status="error",
            error="Conflict",
            detail=detail
        ).model_dump()
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handler for general SQLAlchemy errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            status="error",
            error="Database error",
            detail="An unexpected database error occurred"
        ).model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unexpected exceptions."""
    # Log the actual error for debugging
    import logging
    logging.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            status="error",
            error="Internal server error",
            detail="An unexpected error occurred"
        ).model_dump()
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""
    from fastapi.exceptions import HTTPException
    
    # Custom API errors
    app.add_exception_handler(APIError, api_error_handler)
    
    # Validation errors
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    
    # Database errors
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    
    # HTTP exceptions
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                status="error",
                error=exc.detail or "HTTP error",
                detail=None
            ).model_dump()
        )
