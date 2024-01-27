from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up Jinja2 templates. Assumes your templates are in a folder named "templates"
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/index", response_class=HTMLResponse)
def get_welcome(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def get_welcome(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.get("/register", response_class=HTMLResponse)
def get_welcome(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

