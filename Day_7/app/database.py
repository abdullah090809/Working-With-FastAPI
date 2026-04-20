from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="postgresql://postgres:abdullah1234@localhost/FastAPI"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionMaker = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    db =  SessionMaker()
    try:
        yield db
    finally:
        db.close()