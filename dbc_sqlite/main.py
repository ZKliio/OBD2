# app.py
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    models = query_db("SELECT DISTINCT manufacturer, model, car_model_id FROM dbc_files")
    messages = []
    if model_id:
        messages = query_db("SELECT car_model_id, id, name, dlc, sender, message_id FROM messages WHERE car_model_id = ?", (model_id,))
    return templates.TemplateResponse("select_model.html", {
        "request": request,
        "car_models": models,
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

@app.get("/search", response_class=HTMLResponse)
def shared_messages(request: Request, manufacturer: str = Query(None)):
    # For dropdown filter
    manufacturers = query_db("SELECT DISTINCT manufacturer FROM messages ORDER BY manufacturer")

    # Main query
    sql = """

    WITH shared_messages AS (
        SELECT 
            manufacturer,
            message_id,
            COUNT(DISTINCT car_model) AS model_count
        FROM messages
        GROUP BY manufacturer, message_id
        HAVING model_count > 1
    ),
    ranked_shared AS (
        SELECT *,
            RANK() OVER (PARTITION BY manufacturer ORDER BY model_count DESC) AS rank
        FROM shared_messages
    ),
    message_names AS (
        SELECT 
            manufacturer,
            message_id,
            name,
            COUNT(*) AS name_count
        FROM messages
        GROUP BY manufacturer, message_id, name
    ),
    most_common_names AS (
        SELECT *
        FROM (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY manufacturer, message_id
                    ORDER BY name_count DESC
                ) AS name_rank
            FROM message_names
        )
        WHERE name_rank = 1
    )
    SELECT 
        rs.manufacturer, 
        rs.message_id, 
        mcn.name AS message_name,
        rs.model_count,
        mcn.name_count AS frequency
    FROM ranked_shared rs
    JOIN most_common_names mcn
        ON rs.manufacturer = mcn.manufacturer AND rs.message_id = mcn.message_id
    WHERE rs.rank = 1

    """
    # params = ()
    # if manufacturer:
    #     sql += " AND rs.manufacturer = ?"
    #     params = (manufacturer,)

    # sql += " ORDER BY mcn.name_count DESC"
        
    # sql += " ORDER BY frequency DESC"
    results = query_db(sql)
    # results = query_db(sql, params)
    # print("FINAL SQL:\n", sql)
    # print("PARAMS:", params)
    # Get filtered messages again for second table
    manufacturer_messages = []
    if manufacturer:
        manufacturer_messages = query_db("""
            SELECT message_id, name AS message_name, COUNT(DISTINCT car_model) AS model_count
            FROM messages
            WHERE manufacturer = ?
            GROUP BY message_id, name
            ORDER BY model_count DESC
        """, (manufacturer,))

    return templates.TemplateResponse("shared_messages.html", {
        "request": request,
        "messages": results,
        "manufacturers": manufacturers,
        "selected_manufacturer": manufacturer,
        "manufacturer_messages": manufacturer_messages
    })