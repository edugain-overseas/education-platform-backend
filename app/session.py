from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.setting import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
