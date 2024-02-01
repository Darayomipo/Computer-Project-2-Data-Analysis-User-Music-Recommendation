from typing import List
from datetime import datetime
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import User, SessionLocal, Base
import hashlib

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UserCreate:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/", response_class=HTMLResponse)
def get_welcome(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register/", response_class=HTMLResponse)
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
def register_user(request: Request,
    username: str = Form(...), 
    email: str = Form(...),
    country: str = Form(...),
    age: int = Form(...),
    password: str = Form(...),
    music_genres: List[str] = Form(...),  # Receive music genres as a list
    db: Session = Depends(get_db)
):
    if not 3 <= len(music_genres) <= 5:
        raise HTTPException(status_code=400, detail="Select 3 to 5 music genres.")

    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, country=country, age=age, hashed_password=hashed_password, RegistrationDate=datetime.now())
    db_user.set_genres(music_genres)  # Set the music genres
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return templates.TemplateResponse("registration_complete.html", {"request": request, "username": username})



@app.get("/login/", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    db_user = db.query(User).filter(User.username == username, User.hashed_password == hashed_password).first()
    if db_user:
        music_genres = db_user.get_genres()
        return templates.TemplateResponse("welcome.html",{"request": request, "username": username, "music_genres": music_genres})
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
