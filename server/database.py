from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv


HOST = getenv("POSTGRES_HOST")
USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
DATABASE = getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



