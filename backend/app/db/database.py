from typing import Annotated
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from fastapi import Depends
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

