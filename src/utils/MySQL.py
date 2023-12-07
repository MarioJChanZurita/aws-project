from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from . import DB_URL


class Base(DeclarativeBase):
    ...

class MySQL():

    def __init__(self):
        self.engine = create_engine(DB_URL)
        
    def __enter__(self):
        SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, *_):
        self.db.close()