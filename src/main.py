from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from db.db import create_table, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    # await delete_tables()

app = FastAPI(lifespan=lifespan)


# app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)