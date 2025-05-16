from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from config import settings
from auth.routers import auth_jwt_router
from db import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Выполняется при запуске программы."""
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_jwt_router, prefix=settings.api_prefix.v1)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
