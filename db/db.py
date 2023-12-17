from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import config

Base = declarative_base()
engine = create_async_engine(config.DB_CONNECTION_URL, echo=True)

Base.metadata.create_all(engine)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
