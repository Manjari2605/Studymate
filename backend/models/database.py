from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./data/studymate.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id         = Column(Integer, primary_key=True, index=True)
    filename   = Column(String, nullable=False)
    subject    = Column(String, default="General")
    content    = Column(Text, nullable=False)
    file_size  = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Chunk(Base):
    __tablename__ = "chunks"

    id       = Column(Integer, primary_key=True, index=True)
    note_id  = Column(Integer, nullable=False)
    text     = Column(Text, nullable=False)
    faiss_id = Column(Integer, nullable=False)


class Quiz(Base):
    __tablename__ = "quizzes"

    id         = Column(Integer, primary_key=True, index=True)
    note_id    = Column(Integer, nullable=False)
    question   = Column(Text, nullable=False)
    options    = Column(Text, nullable=False)   # JSON string
    answer     = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
