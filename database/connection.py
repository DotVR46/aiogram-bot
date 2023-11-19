import os
from sqlalchemy import String, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = create_engine(f"sqlite:///{BASE_DIR}/db.sqlite")


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String(255))
    post_url: Mapped[str] = mapped_column(String(255))
    posted = Column(Boolean, default=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
