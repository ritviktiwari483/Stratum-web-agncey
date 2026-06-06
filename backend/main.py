from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3, os

app = Flask(__name__)
CORS(app)

DB = os.path.join(os.path.dirname(__file__), "leads.db")

def init():
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, message TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)")
init()

@app.route("/")
def home():
    return jsonify({"status": "ok"})

@app.route("/api/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return jsonify({"message": "Use POST to submit the form, or visit /admin to view leads"})
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"status": "error", "message": "Name and email required"}), 400
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO leads (name, phone, email, message) VALUES (?,?,?,?)",
                     (data["name"], data.get("phone",""), data["email"], data.get("message","")))
    return jsonify({"status": "success", "message": "Thanks! We'll be in touch."})

@app.route("/admin")
def admin():
    with sqlite3.connect(DB) as conn:
        leads = conn.execute("SELECT * FROM leads ORDER BY date DESC").fetchall()
    rows = "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4][:50]}</td><td>{r[5]}</td></tr>" for r in leads)
    return render_template_string("""
    <!DOCTYPE html><html><head>
    <title>Leads</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      *{margin:0;padding:0;box-sizing:border-box}
      body{font-family:-apple-system,sans-serif;background:#0b1120;color:#f1f5f9;padding:32px}
      h1{color:#d4af37;margin-bottom:24px}
      table{width:100%;border-collapse:collapse;background:#1a2332;border-radius:12px;overflow:hidden}
      th{background:#0f172a;color:#94a3b8;text-align:left;padding:12px 16px;font-size:11px;text-transform:uppercase}
      td{padding:12px 16px;border-top:1px solid #1e293b;font-size:14px}
      tr:hover td{background:#0f172a}
      .count{color:#94a3b8;margin-bottom:16px}
    </style></head><body>
    <h1>Leads ({{ leads|length }})</h1>
    <table><thead><tr><th>#</th><th>Name</th><th>Phone</th><th>Email</th><th>Message</th><th>Date</th></tr></thead>
    <tbody>{{ rows|safe }}</tbody></table></body></html>
    """, leads=leads, rows=rows)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
