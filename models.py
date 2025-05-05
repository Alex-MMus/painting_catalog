from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import Base

class Painting(Base):
    __tablename__ = "paintings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    artist = Column(String)
    price = Column(Float)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    token = Column(String, unique=True)

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    title = Column(String, ForeignKey("paintings.title"))

