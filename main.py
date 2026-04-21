from fastapi import FastAPI, Request
#this is the import used for redirecting the user's url to another shorter url 
from fastapi.responses import RedirectResponse 

#random letters :)  ID which helps to remember and redirect when url is given ...
import string
import random

#saved the url and its id for permanent 
import json
import os

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

#database hai yo chai .... 
DB_FILE = "urls.json"

#uses to load the saved urls ...
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f) #conversion into dictionrry 
        except:
            return {}     
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

url_db = load_data()

def generate_id(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class URLRequest(BaseModel):
    long_url: str
    custom_id: Optional[str] = None

@app.get("/")
def home():
    return {"message": "URL Shortener API Running"}

@app.post("/shorten")
def shorten_url(data: URLRequest, request: Request):
    
    #use custom id if provided else generate
    short_id = data.custom_id if data.custom_id else generate_id()

    #check if already exists
    if short_id in url_db:
        return {"error": "Short ID already exists, try another"}

    #store url + clicks
    url_db[short_id] = {
        "url": data.long_url,
        "clicks": 0
    }

    save_data(url_db)

    return {"short_url": f"{request.base_url}{short_id}"}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    if short_id in url_db:
        url_db[short_id]["clicks"] += 1
        save_data(url_db)
        return RedirectResponse(url_db[short_id]["url"])
    return {"error": "URL not found"}

@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    if short_id in url_db:
        return url_db[short_id]
    return {"error": "Not found"}