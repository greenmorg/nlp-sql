import uvicorn

from fastapi import Depends, FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError

from src.api.models import *
from src.db.models import get_db, DBEmbedding, create_embedding
from src.db.schemas import EmbeddingSchema
from src.db.search import Searcher, EmbeddingSearchResult, StringSearchResult
from src.utils.fetcher import fetch_full_schema
from src.utils.tokenizer import text_to_embedding, embedding_to_text
from src.utils.openai_utils import generate_sql 

origins = [
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

templates = Jinja2Templates(directory="src/api/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/supported_db_drivers", response_class=HTMLResponse)
async def supported_db_drivers():
    drivers = ["postgresql", "mysql", "sqlite", "oracle"]
    options_html = ''.join([f'<option value="{driver}">{driver}</option>' for driver in drivers])
    return HTMLResponse(content=options_html)

@app.post("/schema/fetch", response_class=HTMLResponse)
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
    try:
        schema_str = fetch_full_schema(connection_string)
    except OperationalError as e:
        return templates.TemplateResponse("db/error.html", {"request": request,  "message": "Invalid database credentials. Please try again."})
    return templates.TemplateResponse("schema/fetch.html",  {"request": request, "schema": schema_str})

@app.post("/schema/add", response_class=HTMLResponse)
def add_schema(request: Request, schema: str = Form(...)):
    return templates.TemplateResponse("schema/add.html", {"request": request, "schema": schema})

@app.post("/schema/add/submit")
async def submit_schema(request: Request, name: str = Form(...), content: str = Form(...), db: AsyncSession = Depends(get_db)):
    tokens = text_to_embedding(content)
    print()
    print(f'tokens: {tokens}, lenght: {len(tokens)}')
    print()
    embedding_schema = EmbeddingSchema(name=name, embeddings=tokens)
    db_embedding = await create_embedding(db=db, embedding=embedding_schema)    
    # TODO: redirect    
    return {"message": "Success"}

@app.get("/schemas", response_class=HTMLResponse)
async def get_schemas(request: Request, db: AsyncSession = Depends(get_db)):
    schema_names = await db.execute(select(DBEmbedding.name).distinct())
    options_html = ''.join([f'<option value="{schema.name}">{schema.name}</option>' for schema in schema_names])
    return HTMLResponse(content=options_html)


@app.get("/search")
async def get_search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search")
async def get_search_results(request: Request, user_prompt: str = Form(...), db: AsyncSession = Depends(get_db)):
    searcher = Searcher(db)
    similar_schemas: list[EmbeddingSearchResult] = await searcher.search(user_prompt)
    # print(f'similar schemas: {similar_schemas}')
    similar_schemas: list[StringSearchResult] = [e.to_string_result() for e in similar_schemas]
    return {
        "schemas": [{"content": s.content} for s in similar_schemas]
    }

@app.post("/generate_sql")
async def generate_sql_endpoint(request: Request, user_prompt: str = Form(...), db: AsyncSession = Depends(get_db)):
    search_results = await get_search_results(request, user_prompt=user_prompt, db=db)
    schema_contents = [schema['content'] for schema in search_results['schemas']]
    if not schema_contents:
        raise HTTPException(status_code=404, detail="No relevant schemas found.")
    combined_schemas = "\n".join(schema_contents)
    sql_response = await generate_sql("SQL", combined_schemas, user_prompt)
    return sql_response

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
