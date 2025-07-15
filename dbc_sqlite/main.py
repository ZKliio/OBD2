# app.py
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def query_db(query, params=()):
    conn = sqlite3.connect("can.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()
    return results

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@app.get("/car/messages", response_class=HTMLResponse)
def show_messages(request: Request, model_id: int = Query(None)):
    car_models = query_db("SELECT id, name FROM car_models")
    messages = []
    if model_id:
        messages = query_db("SELECT id, name FROM messages WHERE car_model_id = ?", (model_id,))
    return templates.TemplateResponse("select_model.html", {
        "request": request,
        "car_models": car_models,
        "selected_model": model_id,
        "messages": messages
    })

@app.get("/messages/{message_id}/signals", response_class=HTMLResponse)
def view_signals(request: Request, message_id: int):
    message = query_db("SELECT * FROM messages WHERE id = ?", (message_id,))
    signals = query_db("SELECT * FROM signals WHERE message_id = ?", (message_id,))
    return templates.TemplateResponse("signals.html", {
        "request": request,
        "message": message[0] if message else None,
        "signals": signals
    })
