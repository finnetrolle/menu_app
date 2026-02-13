"""
FastAPI application entry point.
Configures middleware, routes, and exception handlers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import get_settings
from src.api.routes import api_router
from src.api.middleware import register_exception_handlers
from src.database_init import init_database, check_database_connection

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes database connection and seeds initial data on startup.
    """
    # Startup: Initialize database
    print("Starting up...")
    
    # Wait for database connection
    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        if check_database_connection():
            print("Database connection established")
            break
        retry_count += 1
        print(f"Waiting for database... (attempt {retry_count}/{max_retries})")
        import asyncio
        await asyncio.sleep(2)
    
    if retry_count == max_retries:
        print("Warning: Could not establish database connection")
    else:
        # Initialize database with seed data
        init_database()
    
    yield
    
    # Shutdown: cleanup if needed
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="API for managing dishes, ingredients, and nutrition calculations",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Include API routes
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint - redirects to API docs."""
    return {
        "message": "Menu Management API",
        "docs": "/docs",
        "version": "2.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
