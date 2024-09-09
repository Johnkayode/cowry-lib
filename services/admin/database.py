from decouple import AutoConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

config = AutoConfig()

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


