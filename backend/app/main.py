"""
- Start FastAPI application.
- Initialize database file if it doesn't exist.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.media import router as media_router
from app.api.routes.sales import router as sales_router
from app.api.error_handlers import register_error_handlers
from app.core.init_db import init_db


def create_app() -> FastAPI:
    """
    Declare FastAPI application:
    - Add middleware for easy access - future build will require authentication.
    - Initialize sqlite database if not present already.
    - Include routers for API endpoints.
    - Register error handlers.
    - Start an app with root endpoint `/` showing complete status.
    """
    app = FastAPI(title="StoreFlow API", version="1.0")

    # Allow requests originating from any source
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize database
    init_db()

    # Routes
    app.include_router(media_router)
    app.include_router(sales_router)

    # Error handlers
    register_error_handlers(app)

    return app


# Start the application
app = create_app()


@app.get("/")
def root():
    return {"status": "Everything works, Access /docs for API"}
