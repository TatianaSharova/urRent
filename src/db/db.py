from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from config import settings
from models import Base


class DatabaseHelper:
    '''Класс настроек движка бд.'''
    def __init__(self, url: str, echo: bool = False):
        '''
        Создает асинхронный движок, который отвечает
        за подключение к базе данных, и асинхронные сессии.
        '''
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        '''
        Создает scope-сессию — обертку, которая создает
        одну сессию на текущую асинхронную задачу.
        '''
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession,
                                                         None]:
        '''Создает новую сессию при каждом запросе.'''
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncGenerator[AsyncSession,
                                                                None]:
        '''Создает scope-сессию при каждом запросе.'''
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)

async def create_table():
    '''Создает таблицы в бд.'''
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    '''Удаляет таблицы в бд.'''
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# async def get_db() -> AsyncGenerator[AsyncSession, None]:     является session_dependency
#     async with db_helper.session_factory() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
