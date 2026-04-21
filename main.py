from fastapi import FastAPI  #framework...
#this is the import used for redirecting the user's url to another shorter url 
from fastapi.responses import RedirectResponse 
from fastapi.responses import HTMLResponse
#random letters :)  ID which helps to remember and redirect when url is given ...
import string
import random

#saved the url and its id for permanent 
import json
import os

from pydantic import BaseModel

app = FastAPI()

#database hai yo chai .... 
DB_FILE = "urls.json"

#uses to load the saved urls ...
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f) #conversion into dictionrry 
            #file handling 
        except:
            return {}     
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

url_db = load_data()

def generate_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class URLRequest(BaseModel):
    long_url: str

@app.get("/")
def home():
    return {"message": "URL Shortener API Running"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_id = generate_id()
    url_db[short_id] = request.long_url
    save_data(url_db)
    return {"short_url": f"{request.base_url}{short_id}"}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    if short_id in url_db:
        return RedirectResponse(url_db[short_id])
    return {"error": "URL not found"}


@app.get("/app", response_class=HTMLResponse)
def website():
    with open("index.html") as f:
        return f.read()