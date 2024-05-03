from typing import List

from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session,joinedload
import hashlib

from datetime import datetime

# Assuming models.py contains the SQLAlchemy models including User, and SessionLocal for DB session management
from models import User, SessionLocal, Base, UserListeningHistory
from models import Song

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/", response_class=HTMLResponse)
def get_welcome(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register/", response_class=HTMLResponse)
def get_register(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
async def register_user(request: Request,
                        username: str = Form(...), 
                        email: str = Form(...),
                        country: str = Form(...),
                        age: int = Form(...),
                        password: str = Form(...),
                        music_genres: List[str] = Form(...),
                        db: Session = Depends(get_db)):
    if not 3 <= len(music_genres) <= 5:
        raise HTTPException(status_code=400, detail="Select 3 to 5 music genres.")

    db_user = db.query(User).filter(User.Email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(password)
    db_user = User(Username=username, Email=email, Country=country, Age=age, HashedPassword=hashed_password, RegistrationDate=datetime.now())
    db_user.set_genres(music_genres)
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return templates.TemplateResponse("registration_complete.html", {"request": request, "username": username})
#Template gotten from chatGpt but editted  to serve my purpose
@app.get("/login/", response_class=HTMLResponse)
def get_login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    db_user = db.query(User).filter(User.Username == username, User.HashedPassword == hashed_password).first()
    if db_user:
        music_genres = db_user.get_genres()
        age = db_user.Age
        country = db_user.Country
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username, "music_genres": music_genres, "age": age, "country": country})
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
@app.get("/songs/genre/{genre}", response_class=HTMLResponse)
async def read_songs_by_genre(request: Request, genre: str, db: Session = Depends(get_db)):
    songs = db.query(Song).filter(Song.Genre == genre).all()
    if not songs:
        raise HTTPException(status_code=404, detail="Songs not found")
    # Pass the list of songs and the genre to the template
    return templates.TemplateResponse("genre_filter.html", {"request": request,"songs": songs, "genre": genre})




#Template gotten from chatGpt but editted  to serve my purpose
@app.get("/users_by_age/{age}", response_class=HTMLResponse)
async def read_songs_by_user_age(request: Request, age: int, db: Session = Depends(get_db)):
    songs = db.query(Song).join(UserListeningHistory, UserListeningHistory.SongID == Song.SongID)\
                          .join(User, User.UserID == UserListeningHistory.UserID)\
                          .filter(User.Age == age).all()

    if not songs:
        message = f"No users found at this age: {age}"
        return templates.TemplateResponse("age_filter.html", {"request": request, "songs": [], "age": age, "message": message})

    return templates.TemplateResponse("age_filter.html", {"request": request,"songs": songs, "age": age,"message": ""})


@app.get("/users_by_location/{location}", response_class=HTMLResponse)
async def read_songs_by_location(request: Request, location: str, db: Session = Depends(get_db)):
    songs = (db.query(Song)
             .join(UserListeningHistory, UserListeningHistory.SongID == Song.SongID)
             .join(User, User.UserID == UserListeningHistory.UserID)
             .filter(User.Country == location) 
             .all())

    if not songs:
        message = f"No songs found for users in this location: {location}"
        return templates.TemplateResponse("location_filter.html", {"request": request, "songs": [], "location": location, "message": message})

    return templates.TemplateResponse("location_filter.html", {"request": request, "songs": songs, "location": location, "message": ""})


@app.get("/song/{song_id}", response_class=HTMLResponse)
async def read_song_details(request: Request, song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.SongID == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return templates.TemplateResponse("song_detail.html", {"request": request, "song": song})


