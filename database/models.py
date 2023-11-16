from sqlalchemy import String, Boolean, Column
from database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String(255))
    post_url: Mapped[str] = mapped_column(String(255))
    posted = Column(Boolean, default=False)
