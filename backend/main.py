from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3, os, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

app = Flask(__name__)
CORS(app)

DB = os.environ.get("DATABASE_URL", os.path.join(os.path.dirname(__file__), "leads.db"))
ADMIN_PASSWORD = "stratum_admin" # Change this to your preferred password

# EMAIL SETTINGS (User needs to provide these)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "startumweb@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "") # App Password
RECEIVER_EMAIL = "startumweb@gmail.com"

def init(db_path=DB):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                phone TEXT, 
                email TEXT, 
                country TEXT,
                message TEXT, 
                ip_address TEXT,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Ensure 'ip_address' and 'country' columns exist
        for col in ["country", "ip_address"]:
            try:
                conn.execute(f"ALTER TABLE leads ADD COLUMN {col} TEXT")
            except sqlite3.OperationalError:
                pass 

def send_email_notification(lead_data):
    if not SENDER_PASSWORD:
        print("Email notification skipped: SENDER_PASSWORD not set.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚀 New Lead: {lead_data['name']} (StratumWeb)"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
                <div style="background: #1a1a1a; padding: 20px; text-align: center;">
                    <h1 style="color: #d4af37; margin: 0;">New Lead Captured</h1>
                </div>
                <div style="padding: 20px;">
                    <p>Details of the new inquiry:</p>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Name:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{lead_data['name']}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{lead_data['email']}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Phone:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{lead_data['phone']}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Country:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{lead_data['country']}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>IP:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{lead_data['ip_address']}</td></tr>
                    </table>
                    <div style="margin-top: 20px; padding: 15px; background: #f9f9f9; border-left: 4px solid #d4af37;">
                        <strong>Message:</strong><br>{lead_data['message']}
                    </div>
                </div>
                <div style="background: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; color: #888;">
                    &copy; 2026 StratumWeb Agency - Automated Notification
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email notification sent for lead: {lead_data['email']}")
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")

@app.route("/")
def home():
    return jsonify({
        "status": "active",
        "service": "StratumWeb Backend",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/admin")
def admin():
    pwd = request.args.get("pass")
    if pwd != ADMIN_PASSWORD:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login - StratumWeb</title>
            <style>
                body { font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .login-card { background: #1e293b; padding: 40px; border-radius: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 100%; max-width: 400px; text-align: center; }
                h1 { color: #facc15; margin-bottom: 24px; font-size: 24px; }
                input { width: 100%; padding: 12px; margin-bottom: 16px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
                button { width: 100%; padding: 12px; border-radius: 8px; border: none; background: #facc15; color: #0f172a; font-weight: bold; cursor: pointer; transition: 0.3s; }
                button:hover { background: #eab308; }
            </style>
        </head>
        <body>
            <div class="login-card">
                <h1>Admin Access</h1>
                <form action="/admin" method="get">
                    <input type="password" name="pass" placeholder="Enter Access Password" required>
                    <button type="submit">LOGIN TO DASHBOARD</button>
                </form>
            </div>
        </body>
        </html>
        """, 403
    
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            leads = conn.execute("SELECT * FROM leads ORDER BY date DESC").fetchall()
        
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>StratumWeb | Premium Admin Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
                body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0c0f18; color: #e2e8f0; }
                .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); }
                .gold-gradient { background: linear-gradient(135deg, #d4af37 0%, #facc15 100%); }
                .lead-row:hover { background: rgba(255, 255, 255, 0.03); }
            </style>
        </head>
        <body class="p-6 md:p-12">
            <div class="max-w-7xl mx-auto">
                <header class="flex flex-col md:flex-row justify-between items-center mb-12 gap-6">
                    <div>
                        <h1 class="text-3xl font-extrabold tracking-tight">Lead <span class="text-yellow-500">Intelligence</span></h1>
                        <p class="text-slate-400 mt-1">Real-time engagement tracking for StratumWeb Agency</p>
                    </div>
                    <div class="flex gap-4">
                        <div class="glass px-6 py-3 rounded-2xl text-center">
                            <p class="text-xs text-slate-500 uppercase tracking-widest font-bold">Total Leads</p>
                            <p class="text-2xl font-bold text-yellow-500">{{ count }}</p>
                        </div>
                        <button onclick="window.location.reload()" class="glass h-full px-6 rounded-2xl hover:bg-slate-700 transition-all">
                            <i class="fa-solid fa-rotate"></i>
                        </button>
                    </div>
                </header>

                <div class="glass rounded-[32px] overflow-hidden shadow-2xl">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead>
                                <tr class="bg-slate-800/50 text-slate-400 text-xs uppercase tracking-widest font-bold">
                                    <th class="px-8 py-6">Timestamp</th>
                                    <th class="px-8 py-6">Client Identity</th>
                                    <th class="px-8 py-6">Contact Info</th>
                                    <th class="px-8 py-6">Origin</th>
                                    <th class="px-8 py-6">Project Brief</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800">
                                {% for lead in leads %}
                                <tr class="lead-row transition-colors">
                                    <td class="px-8 py-8 whitespace-nowrap">
                                        <div class="text-sm font-medium">{{ lead['date'].split(' ')[0] }}</div>
                                        <div class="text-[10px] text-slate-500 mt-1">{{ lead['date'].split(' ')[1] }}</div>
                                    </td>
                                    <td class="px-8 py-8">
                                        <div class="text-base font-bold text-white">{{ lead['name'] }}</div>
                                        <div class="text-xs text-yellow-500/80 mt-1">Potential Client</div>
                                    </td>
                                    <td class="px-8 py-8">
                                        <div class="flex flex-col gap-2">
                                            <div class="flex items-center gap-2 text-sm">
                                                <i class="fa-solid fa-envelope text-[10px] text-slate-500"></i>
                                                {{ lead['email'] }}
                                            </div>
                                            <div class="flex items-center gap-2 text-sm">
                                                <i class="fa-solid fa-phone text-[10px] text-slate-500"></i>
                                                {{ lead['phone'] }}
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-8 py-8">
                                        <span class="px-3 py-1 bg-yellow-500/10 text-yellow-500 rounded-full text-xs font-bold">{{ lead['country'] }}</span>
                                        <div class="text-[10px] text-slate-600 mt-2 font-mono uppercase">{{ lead['ip_address'] }}</div>
                                    </td>
                                    <td class="px-8 py-8">
                                        <p class="text-sm text-slate-300 max-w-xs line-clamp-2 hover:line-clamp-none cursor-help transition-all">
                                            {{ lead['message'] }}
                                        </p>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>

                <footer class="mt-12 text-center text-slate-600 text-xs uppercase tracking-[0.2em]">
                    &copy; 2026 STRATUMWEB INTERNAL INFRASTRUCTURE &bull; SECURITY LEVEL: ALPHA
                </footer>
            </div>
        </body>
        </html>
        """
        return render_template_string(html, leads=leads, count=len(leads))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"status": "error", "message": "Name and email are required"}), 400
    
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone", "")
    country = data.get("country", "")
    message = data.get("message", "")
    
    ip_address = request.remote_addr if not request.headers.get('X-Forwarded-For') else request.headers.get('X-Forwarded-For').split(',')[0]

    lead_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "country": country,
        "message": message,
        "ip_address": ip_address
    }

    try:
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO leads (name, phone, email, country, message, ip_address) VALUES (?,?,?,?,?,?)",
                (name, phone, email, country, message, ip_address)
            )
        
        # Log to File
        with open(os.path.join(os.path.dirname(__file__), "leads_log.txt"), "a") as f:
            f.write(f"\n[{datetime.now()}] NEW LEAD: {name} ({email}) - {country}\n")

        # Async Email Notification
        threading.Thread(target=send_email_notification, args=(lead_data,)).start()
        
        return jsonify({
            "status": "success", 
            "message": f"Success! Thank you, {name}. We've received your inquiry."
        })
    except Exception as e:
        error_msg = f"ERROR STORING LEAD: {str(e)}"
        print(error_msg)
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    init()
    app.run(debug=True, host="0.0.0.0", port=8000)
else:
    init()


