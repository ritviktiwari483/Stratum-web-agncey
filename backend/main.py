from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3, os

app = FastAPI(title="StratumWeb API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

init_db()

class ContactData(BaseModel):
    name: str
    phone: str
    email: str
    message: str

@app.get("/")
def root():
    return {"status": "ok", "message": "StratumWeb API running"}

@app.post("/api/contact")
def submit_contact(data: ContactData):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO contacts (name, phone, email, message) VALUES (?, ?, ?, ?)",
                 (data.name, data.phone, data.email, data.message))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Thank you! We'll get back to you soon."}

@app.get("/api/contacts")
def get_contacts():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM contacts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "phone": r[2], "email": r[3], "message": r[4], "created_at": r[5]} for r in rows]
