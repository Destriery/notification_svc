from fastapi import FastAPI

from app.router import router

application = FastAPI(
    title="NotificationService",
    description="Author - Destriery",
    version="0.0.1",
)

application.include_router(router)
