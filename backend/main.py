from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB = os.environ.get("DATABASE_URL", os.path.join(os.path.dirname(__file__), "leads.db"))
ADMIN_PASSWORD = "stratum_admin" # Change this to your preferred password

def init(db_path=DB):
    with sqlite3.connect(db_path) as conn:
        # Create table with all necessary fields including ip_address
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

@app.route("/")
def home():
    return jsonify({
        "status": "active",
        "service": "StratumWeb Backend"
    })

@app.route("/admin")
def admin():
    pwd = request.args.get("pass")
    if pwd != ADMIN_PASSWORD:
        return f"<h1>Access Denied</h1><p>Usage: /admin?pass={ADMIN_PASSWORD}</p>", 403
    
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            leads = conn.execute("SELECT * FROM leads ORDER BY date DESC").fetchall()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>StratumWeb Admin Dashboard</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa; padding: 40px; color: #333; }
                h1 { color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
                th { background: #1a1a1a; color: #d4af37; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }
                tr:hover { background: #fffcf0; }
                .ip { font-family: monospace; color: #666; font-size: 12px; }
                .date { color: #888; font-size: 12px; }
            </style>
        </head>
        <body>
            <h1>Lead Submissions ({{ count }})</h1>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Country</th>
                        <th>Message</th>
                        <th>IP Address</th>
                    </tr>
                </thead>
                <tbody>
                    {% for lead in leads %}
                    <tr>
                        <td class="date">{{ lead['date'] }}</td>
                        <td><strong>{{ lead['name'] }}</strong></td>
                        <td>{{ lead['email'] }}</td>
                        <td>{{ lead['phone'] }}</td>
                        <td>{{ lead['country'] }}</td>
                        <td>{{ lead['message'] }}</td>
                        <td class="ip">{{ lead['ip_address'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
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
    # Capture IP Address
    ip_address = request.remote_addr if not request.headers.get('X-Forwarded-For') else request.headers.get('X-Forwarded-For').split(',')[0]

    try:
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO leads (name, phone, email, country, message, ip_address) VALUES (?,?,?,?,?,?)",
                (name, phone, email, country, message, ip_address)
            )
        
        # Format the log entry
        log_entry = (
            "\n" + "="*50 + "\n" +
            f"NEW LEAD RECEIVED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" +
            "="*50 + "\n" +
            f"Name:    {name}\n" +
            f"Email:   {email}\n" +
            f"Phone:   {phone}\n" +
            f"Country: {country}\n" +
            f"IP:      {ip_address}\n" +
            f"Message: {message}\n" +
            "="*50 + "\n"
        )
        
        # Log to Console
        print(log_entry)
        
        # Log to File (Lazy-friendly: just open the file to see leads!)
        with open(os.path.join(os.path.dirname(__file__), "leads_log.txt"), "a") as f:
            f.write(log_entry)
        
        return jsonify({
            "status": "success", 
            "message": f"Success! Thank you, {name}. We've received your inquiry."
        })
    except Exception as e:
        error_msg = f"ERROR STORING LEAD: {str(e)}"
        print(error_msg)
        with open(os.path.join(os.path.dirname(__file__), "leads_log.txt"), "a") as f:
            f.write(f"\n[{datetime.now()}] {error_msg}\n")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    init()
    # Using 0.0.0.0 and port 8000 as previously configured
    app.run(debug=True, host="0.0.0.0", port=8000)
else:
    init()

