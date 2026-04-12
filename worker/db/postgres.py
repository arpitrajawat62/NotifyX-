import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
)
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in environment variables")


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    query = Column(Text, nullable=False)

    frequency = Column(String, default="daily")

    last_checked_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)


def get_user_email(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user.email if user else None
    finally:
        session.close()

def get_active_daily_alerts():
    session = SessionLocal()
    try:
        return (
            session.query(Alert)
            .filter(Alert.is_active.is_(True))
            .filter(Alert.frequency == "daily")
            .all()
        )
    finally:
        session.close()
