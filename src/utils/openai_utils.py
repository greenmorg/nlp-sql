import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('src/utils/.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

with open("src/utils/sql_prompt_template.txt", "r") as file:
    prompt_template = file.read()

async def generate_sql(dialect: str, table_schemas: str, user_prompt: str) -> str:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
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
