import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.getenv("DATABASE_URL")
if db_url:
    engine = create_engine(db_url, pool_size=20, pool_recycle=3600)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()
