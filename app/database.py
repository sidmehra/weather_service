# this is a database connection file 

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

# Create SQLite engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()