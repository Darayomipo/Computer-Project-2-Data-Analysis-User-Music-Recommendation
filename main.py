from typing import List
from datetime import datetime
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import hashlib

# Assuming models.py contains the SQLAlchemy models including User, and SessionLocal for DB session management
from models import User, SessionLocal, Base
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
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    songs = db.query(Song).filter(Song.Genre == genre).all()
    if not songs:
        raise HTTPException(status_code=404, detail="Songs not found")
    # Pass the list of songs and the genre to the template
    return templates.TemplateResponse("genre_filter.html", {"request": request, "songs": songs, "genre": genre})

@app.get("/users_by_age/{age}", response_class=HTMLResponse)
async def read_users_by_age(request: Request, age: int, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.Age == age).all() 
    if not users:
        raise HTTPException(status_code=404, detail="Users of this age not found")

    return templates.TemplateResponse("age_filter.html", {"request": request, "users": users, "age": age})
@app.get("/users_by_location/{location}", response_class=HTMLResponse)
async def read_users_by_age(request: Request, location: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.Country == location).all() 
    if not users:
        raise HTTPException(status_code=404, detail="Users of this location not found")

    return templates.TemplateResponse("location_filter.html", {"request": request, "users": users, "location": location})
