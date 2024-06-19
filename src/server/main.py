import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from .models import *
from ..utils.fetcher import fetch_full_schema
from ..utils.tokenizer import encode, decode, per_byte_decoding

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="src/server/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/supported_db_drivers", response_class=HTMLResponse)
async def supported_db_drivers():
    drivers = ["postgresql", "mysql", "sqlite", "oracle"]
    options_html = ''.join([f'<option value="{driver}">{driver}</option>' for driver in drivers])
    return HTMLResponse(content=options_html)

@app.post("/schema/fetch")
def ask_schema(
    request: Request, 
    host: str = Form(...),
    port: str = Form(...),
    user: str = Form(...),
    password: str = Form(...),
    db_name: str = Form(...),
    driver: str = Form(...)
    ):
    db_details = DatabaseDetails(host=host, port=port, user=user, password=password, driver=driver, db_name=db_name)
    connection_string = db_details.to_connection_string()
    schema_str = fetch_full_schema(connection_string)
    return templates.TemplateResponse("schema/fetch.html",  {"request": request, "schema": schema_str})

@app.post("/schema/add")
def add_schema(request: Request, schema: str = Form(...)):
    return templates.TemplateResponse("schema/add.html", {"request": request, "schema": schema})

    
    


