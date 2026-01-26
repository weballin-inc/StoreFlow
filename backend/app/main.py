from fastapi import FastAPI

from app.api.routes.media import router as media_router
from app.api.error_handlers import register_error_handlers
from app.core.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="StoreFlow API", version="0.6.7")

    # Initialize database
    init_db()

    # Routes
    app.include_router(media_router)

    # Error handlers
    register_error_handlers(app)

    return app

app = create_app()

@app.get("/")
def root():
    return {"status": "Everything works, Access /docs for API"}
