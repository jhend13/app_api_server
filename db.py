from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine("postgresql+psycopg://postgres:root@localhost:5432/aadd", echo=True)

SessionLocal = sessionmaker(engine)