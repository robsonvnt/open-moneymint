import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.repository.user_db_repository import Base

db_url = os.getenv("DATABASE_URL")
env = os.getenv("ENV", "development")
if db_url:
    engine = create_engine(db_url, pool_size=20, pool_recycle=3600)
    if env == "development":
        Base.metadata.create_all(bind=engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()