import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_session():
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()
    try:
        yield db
    finally:
        db.close()