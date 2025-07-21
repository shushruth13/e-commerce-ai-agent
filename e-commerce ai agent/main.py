from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import requests
import os
from fastapi.responses import HTMLResponse

# FastAPI app
app = FastAPI()

# SQLite DB path
DB_PATH = 'focus_data.db'

# Ollama API settings
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sql: str
    data: list

# Helper: Call Llama 3 via Ollama to translate question to SQL

def question_to_sql(question: str) -> str:
    schema = '''
Tables and columns:
- total_sales_metrics(date, item_id, total_sales, total_units_ordered)
- ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- eligibility_table(eligibility_datetime_utc, item_id, eligibility, message)
'''
    prompt = f"""
Given the tables and columns below, write a concise SQLite SQL query to answer the question. Use ONLY these tables/columns. NEVER invent new tables/columns. If not possible, reply: ERROR: Cannot answer with available tables. Output ONLY the SQL query, nothing else.

{schema}
Question: {question}
"""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")
    sql = response.json().get('response', '').strip()
    # Remove code block markers if present
    if sql.startswith('```'):
        sql = sql.split('```')[1].strip()
    return sql

# Helper: Execute SQL and fetch results
def run_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        return data
    finally:
        conn.close()

# Helper: Format answer for user
def format_answer(data):
    if not data:
        return "No results found."
    # Show as table
    keys = data[0].keys()
    lines = [" | ".join(keys)]
    lines.append("-|-" * len(keys))
    for row in data:
        lines.append(" | ".join(str(row[k]) for k in keys))
    return "\n".join(lines)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>Welcome to the AI Data Q&A API!</h2>
    <p>Use the <a href='/docs'>/docs</a> to try the /ask endpoint.<br>
    Or connect via the frontend app to ask questions about your data.</p>
    """

@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    try:
        sql = question_to_sql(req.question)
        data = run_sql(sql)
        answer = format_answer(data)
        return AnswerResponse(answer=answer, sql=sql, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 