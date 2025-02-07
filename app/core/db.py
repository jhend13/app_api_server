from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+psycopg://postgres:root@localhost:5432/aadd", echo=True)

SessionLocal = sessionmaker(engine)
