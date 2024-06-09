import os
import contextlib
from typing import Any, AsyncIterator


from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from exceptions.database import DBEngineException

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine: AsyncEngine | None = create_async_engine(host, **engine_kwargs)
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = (
            async_sessionmaker(autocommit=False, bind=self._engine)
        )

    async def close(self) -> None:
        if self._engine is None:
            raise DBEngineException("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DBEngineException("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# TODO: Should be removed ASAP
DB_USERNAME = "cells-backend"
DB_SECRET = "82I14CNHA0ZnxW7"
DB_HOST = (
    "postgres.default.svc.cluster.local"
    if os.environ.get("DEV") == "false"
    else "0.0.0.0"
)
DB_PORT = "5432"
DB_NAME = "cells-db"

session_manager = DatabaseSessionManager(
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_SECRET}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    {"future": True, "echo": True},
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session
