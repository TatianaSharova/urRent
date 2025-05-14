from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from config import settings
from db.db_helper import create_table, delete_tables  # noqa: F401
from auth.routers import auth_jwt_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Выполняется при запуске программы."""
    await create_table()
    yield
    # await delete_tables()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_jwt_router, prefix=settings.api_prefix.v1)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
