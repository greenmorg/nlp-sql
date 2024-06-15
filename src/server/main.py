import os

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

import tiktoken

from .models import *

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

encoder = tiktoken.get_encoding("cl100k_base")

@app.get("/")
def index():
    return {
        "message": "Wrong path. Please, proceed to the /sql_query."
    }

@app.post("/add_schema")
def add_schema(request_schema: RequestSchema):
    tokens = encoder.encode(request_schema.content)
    return {
        "tokens": tokens,
        "decoded": [encoder.decode_single_token_bytes(t) for t in tokens]
    }
        
@app.post("/sql_query")
def ask_schema(request: Request):
    return {
        "message": "Everything is fine..."
    }
    


