from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

class Tea(Base):
    __tablename__ = 'teas'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    subcategory = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    packaging = Column(String)
    image_url = Column(String)
    link = Column(String)
    weight = Column(String)
    product_id = Column(String, index=True)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    parent = relationship('Category', remote_side=[id])

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, index=True)
    preferences = Column(JSON)
    history = Column(JSON)

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    tea_id = Column(Integer, ForeignKey('teas.id'), index=True)
    rating = Column(Integer)
    comment = Column(String)
    timestamp = Column(DateTime, index=True)

DB_URL = os.getenv('DATABASE_URL')
if not DB_URL:
    raise EnvironmentError('DATABASE_URL environment variable must be set.')
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)