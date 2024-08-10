from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from Database.database import Base

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    movies = relationship("Movie", back_populates="owner")
    comments = relationship("Comment", back_populates="user")

class Movie(Base):
    _tablename_ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie")

class Comment(Base):
    _tablename_ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text)

    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")