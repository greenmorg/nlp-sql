from pydantic import BaseModel
from fastapi.requests import Request

class RequestSchema(BaseModel):
    name: str
    content: str