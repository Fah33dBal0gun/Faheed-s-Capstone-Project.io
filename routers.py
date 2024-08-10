from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .main import get_current_user, users_db
from Database.database import get_db
from passlib.context import CryptContext

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.post("/users/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/movies", response_model=schemas.MovieOut)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = models.Movie(**movie.dict(), owner_id=current_user.id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/movies", response_model=List[schemas.MovieOut])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()

@router.put("/movies/{movie_id}", response_model=schemas.MovieOut)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == current_user.id).first()
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or not owned by user")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/movies/{movie_id}", response_model=schemas.MovieOut)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == current_user.id).first()
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or not owned by user")
    db.delete(db_movie)
    db.commit()
    return db_movie

@router.post("/movies/{movie_id}/comments", response_model=schemas.CommentOut)
def create_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db_comment = models.Comment(**comment.dict(), movie_id=movie_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/movies/{movie_id}/comments", response_model=List[schemas.CommentOut])
def read_comments(movie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()