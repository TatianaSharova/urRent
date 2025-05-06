from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from config import settings
from db.db import create_table, delete_tables
from auth.routers import auth_jwt_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Выполняется при запуске программы.'''
    await create_table()
    yield
    # await delete_tables()

app = FastAPI(lifespan=lifespan)


app.include_router(auth_jwt_router, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
