from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

class Tea(Base):
    __tablename__ = 'teas'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    subcategory = Column(String)
    description = Column(String)
    price = Column(Float)
    packaging = Column(String)
    image_url = Column(String)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    parent = relationship('Category', remote_side=[id])

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    preferences = Column(JSON)
    history = Column(JSON)

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tea_id = Column(Integer, ForeignKey('teas.id'))
    rating = Column(Integer)
    comment = Column(String)
    timestamp = Column(DateTime)

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:48fo27cl@localhost:5432/postgres')
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine) 