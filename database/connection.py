from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db.sqlite")


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
