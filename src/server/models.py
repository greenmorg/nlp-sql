from pydantic import BaseModel
from fastapi.requests import Request

# connection_string = 'postgresql://postgres:mysecretpassword@0.0.0.0:6432/postgres'

class DatabaseDetails(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db_name: str
    driver: str

    def to_connection_string(self):
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
    

class SchemaBase(BaseModel):
    name: str
    content: str

class AddSchema(SchemaBase):
    pass
