import os
from dotenv import load_dotenv
from pathlib import Path
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


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / "backend" / ".env"

load_dotenv(dotenv_path=ENV_PATH)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    query = Column(Text, nullable=False)

    frequency = Column(String)
    source = Column(String)

    last_checked_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean)


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
