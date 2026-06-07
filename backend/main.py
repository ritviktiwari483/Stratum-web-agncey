from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS
import sqlite3, os, smtplib, csv, io
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = Flask(__name__)
# Enable Global CORS for easier mobile/local testing
CORS(app, resources={r"/*": {"origins": "*"}})

# Constants
DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "stratum_admin")
LOG_FILE = os.path.join(os.path.dirname(__file__), "leads_log.txt")

# EMAIL SETTINGS
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "startumweb@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "") # Set in .env
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "startumweb@gmail.com")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        with get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL, 
                    phone TEXT, 
                    email TEXT NOT NULL, 
                    country TEXT,
                    message TEXT, 
                    ip_address TEXT,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Migration check
            cursor = conn.execute("PRAGMA table_info(leads)")
            current_cols = [row[1] for row in cursor.fetchall()]
            for col in ["country", "ip_address"]:
                if col not in current_cols:
                    conn.execute(f"ALTER TABLE leads ADD COLUMN {col} TEXT")
            print("[INFO] Database Initialized Successfully.")
    except Exception as e:
        print(f"[ERROR] Database Initialization Failed: {e}")

def send_email_async(lead_data):
    if not SENDER_PASSWORD: return
    try:
        msg = MIMEMultipart()
        msg['From'] = f"StratumWeb Admin <{SENDER_EMAIL}>"
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"⚡ NEW LEAD: {lead_data['name']}"

        body = f"<h2>New Inquiry from {lead_data['name']}</h2>"
        body += f"<p><strong>Email:</strong> {lead_data['email']}</p>"
        body += f"<p><strong>Phone:</strong> {lead_data['phone']}</p>"
        body += f"<p><strong>Country:</strong> {lead_data['country']}</p>"
        body += f"<p><strong>Message:</strong><br>{lead_data['message']}</p>"
        body += f"<hr><p><small>IP: {lead_data['ip_address']}</small></p>"
        
        msg.attach(MIMEText(body, 'html'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[SMTP ERROR] {e}")

@app.route("/")
def index():
    return jsonify({
        "engine": "StratumWeb Lead Core",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/contact", methods=["POST"])
def capture_lead():
    data = request.json
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    name = data['name']
    email = data['email']
    phone = data.get('phone', 'N/A')
    country = data.get('country', 'Unknown')
    message = data.get('message', '')
    ip = request.remote_addr if not request.headers.get('X-Forwarded-For') else request.headers.get('X-Forwarded-For').split(',')[0]

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO leads (name, email, phone, country, message, ip_address) VALUES (?,?,?,?,?,?)",
                (name, email, phone, country, message, ip)
            )
        
        # Log to file
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] LEAD: {name} | {email} | {country}\n")

        # Email
        threading.Thread(target=send_email_async, args=({
            "name": name, "email": email, "phone": phone, "country": country, "message": message, "ip_address": ip
        },)).start()

        return jsonify({"status": "success", "message": "Lead Captured"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin")
def admin_dashboard():
    password = request.args.get('pass')
    if password != ADMIN_PASSWORD:
        return """
        <body style="background:#0f172a; color:white; font-family:sans-serif; display:flex; align-items:center; justify-content:center; height:100vh;">
            <form style="background:#1e293b; padding:2rem; border-radius:1rem; text-align:center;">
                <h2 style="color:#d4af37">Admin Verification</h2>
                <input type="password" name="pass" style="padding:0.75rem; border-radius:0.5rem; border:none; width:100%; margin-bottom:1rem;" placeholder="Enter Password">
                <button style="background:#d4af37; border:none; padding:0.75rem 1.5rem; border-radius:0.5rem; font-weight:bold; cursor:pointer;">LOGIN</button>
            </form>
        </body>
        """, 403

    try:
        with get_db() as conn:
            leads = conn.execute("SELECT * FROM leads ORDER BY date DESC").fetchall()
        
        # Super-Premium Dashboard Template
        admin_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>StratumWeb | Lead Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
            <style>
                body { background: #0c0f18; color: #e2e8f0; font-family: 'Inter', sans-serif; }
                .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); }
            </style>
        </head>
        <body class="p-8">
            <div class="max-w-6xl mx-auto">
                <div class="flex justify-between items-center mb-10">
                    <div>
                        <h1 class="text-3xl font-bold">Client <span class="text-yellow-500">Pipeline</span></h1>
                        <p class="text-slate-400">Total Leads Handled: <span class="text-white font-bold">{{ count }}</span></p>
                    </div>
                    <a href="/admin/export?pass={{ pwd }}" class="bg-yellow-600 hover:bg-yellow-500 text-white px-6 py-2 rounded-lg font-bold transition">
                        <i class="fa-solid fa-download mr-2"></i> EXPORT CSV
                    </a>
                </div>

                <div class="glass rounded-2xl overflow-hidden">
                    <table class="w-full text-left">
                        <thead class="bg-slate-800 text-slate-400 text-xs uppercase tracking-widest font-bold">
                            <tr>
                                <th class="p-5">Client</th>
                                <th class="p-5">Contact</th>
                                <th class="p-5">Project Focus</th>
                                <th class="p-5">Date</th>
                                <th class="p-5">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for lead in leads %}
                            <tr class="border-t border-white/5 hover:bg-white/5 transition" id="row-{{ lead['id'] }}">
                                <td class="p-5">
                                    <div class="font-bold text-white">{{ lead['name'] }}</div>
                                    <div class="text-xs text-yellow-500/70 uppercase tracking-tighter">{{ lead['country'] }}</div>
                                </td>
                                <td class="p-5 text-sm">
                                    <div class="flex items-center gap-2"><i class="fa-solid fa-envelope text-slate-500"></i> {{ lead['email'] }}</div>
                                    <div class="flex items-center gap-2 mt-1"><i class="fa-solid fa-phone text-slate-500"></i> {{ lead['phone'] }}</div>
                                </td>
                                <td class="p-5">
                                    <p class="text-xs text-slate-300 max-w-xs truncate" title="{{ lead['message'] }}">{{ lead['message'] }}</p>
                                </td>
                                <td class="p-5 text-xs text-slate-500">{{ lead['date'] }}</td>
                                <td class="p-5">
                                    <button onclick="del({{ lead['id'] }})" class="text-slate-600 hover:text-red-500 transition"><i class="fa-solid fa-trash"></i></button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <script>
                async function del(id) {
                    if (!confirm('Permanently delete this record?')) return;
                    const res = await fetch(`/admin/delete/${id}?pass={{ pwd }}`, { method:'POST' });
                    if(res.ok) document.getElementById(`row-${id}`).remove();
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(admin_html, leads=leads, count=len(leads), pwd=password)
    except Exception as e:
        return f"Dashboard Error: {e}", 500

@app.route("/admin/export")
def export():
    password = request.args.get('pass')
    if password != ADMIN_PASSWORD: return "Unauthorized", 403
    try:
        with get_db() as conn:
            leads = conn.execute("SELECT * FROM leads ORDER BY date DESC").fetchall()
        output = io.StringIO()
        w = csv.writer(output)
        w.writerow(["ID", "Name", "Email", "Phone", "Country", "Message", "IP", "Date"])
        for l in leads:
            w.writerow([l['id'], l['name'], l['email'], l['phone'], l['country'], l['message'], l['ip_address'], l['date']])
        return Response(output.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=leads.csv"})
    except Exception as e: return str(e), 500

@app.route("/admin/delete/<int:id>", methods=["POST"])
def delete_item(id):
    password = request.args.get('pass')
    if password != ADMIN_PASSWORD: return "Unauthorized", 403
    try:
        with get_db() as conn:
            conn.execute("DELETE FROM leads WHERE id = ?", (id,))
        return jsonify({"status": "success"})
    except Exception as e: return str(e), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=8000)
else:
    init_db()
