import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base 

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@fastapi_db:5432/job_tracker_db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


