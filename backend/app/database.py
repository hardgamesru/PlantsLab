from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./scooters.db"  # Можно заменить на PostgreSQL/MySQL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # только для SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
