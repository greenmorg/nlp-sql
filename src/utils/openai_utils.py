import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('src/utils/.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_EMB_MODEL = os.getenv("OPENAI_EMB_MODEL")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

with open("src/utils/sql_prompt_template.txt", "r") as file:
    prompt_template = file.read()

async def generate_sql(dialect: str, table_schemas: str, user_prompt: str) -> str:

    prompt = prompt_template.format(
        dialect=dialect,
        table_schemas=table_schemas
    )
    
    chat_completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt},
        ],
    
    )
    
    sql_response = chat_completion.choices[0].message.content.strip()
    return sql_response

async def context_aware_text_to_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=OPENAI_EMB_MODEL
    )
    return response.data[0].embedding