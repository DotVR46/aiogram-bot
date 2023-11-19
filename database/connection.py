import asyncio
import os
from sqlalchemy import String, Boolean, Column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column
from aiosqlite import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite")


async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
session = async_session()


Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String(255))
    post_url: Mapped[str] = mapped_column(String(255))
    posted = Column(Boolean, default=False)

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_all())
