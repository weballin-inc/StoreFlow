from fastapi import FastAPI

from app.api.routes.media import router as media_router
from app.api.routes.copies import router as copies_router
from app.api.routes.sales import router as sales_router

from app.api.error_handlers import register_error_handlers, media_not_found_handler
from app.core.init_db import init_db
from app.domain.exceptions import MediaNotFoundError


def create_app() -> FastAPI:
    app = FastAPI(title="StoreFlow API", version="0.6.7")

    # Initialize database
    init_db()

    # Routes
    app.include_router(media_router)
    app.include_router(copies_router)
    app.include_router(sales_router)

    # Error handlers
    register_error_handlers(app)
    app.add_exception_handler(MediaNotFoundError, media_not_found_handler)

    return app

app = create_app()

@app.get("/")
def root():
    return {"status": "Everything works, Access /docs for API"}
