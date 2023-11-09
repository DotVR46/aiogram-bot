from sqlalchemy import create_engine, String, Boolean, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

engine = create_engine("sqlite:///db.sqlite")


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
