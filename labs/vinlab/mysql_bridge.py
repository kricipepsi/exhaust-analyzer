"""
mysql_bridge.py — local HTTP bridge so the Claude sandbox can query TecDoc.
Run on Windows:  python mysql_bridge.py
Opens an ngrok tunnel automatically and prints the public URL.
Only SELECT / SHOW / DESCRIBE / EXPLAIN are allowed.
"""

import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

import mysql.connector
from pyngrok import ngrok

# ── configure ─────────────────────────────────────────────────────────────────
MYSQL_HOST     = "127.0.0.1"
MYSQL_PORT     = 3306
MYSQL_USER     = "root"
MYSQL_PASSWORD = ""          # fill in if you have a password
MYSQL_DATABASE = "tecdoc"    # change if DB name differs
BRIDGE_PORT    = 8765
# ──────────────────────────────────────────────────────────────────────────────

ALLOWED = re.compile(r"^\s*(SELECT|SHOW|DESCRIBE|DESC|EXPLAIN)\b", re.IGNORECASE)


def run_query(sql: str) -> dict:
    if not ALLOWED.match(sql):
        return {"error": "Only SELECT/SHOW/DESCRIBE/EXPLAIN allowed"}
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST, port=MYSQL_PORT,
            user=MYSQL_USER, password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE, connection_timeout=10
        )
        cur = conn.cursor()
        cur.execute(sql)
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [list(r) for r in cur.fetchall()]
        cur.close()
        conn.close()
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return {"error": str(e)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(fmt % args)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"mysql_bridge running")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            sql = json.loads(body).get("sql", "")
        except Exception:
            sql = ""
        result = run_query(sql)
        payload = json.dumps(result, default=str).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    tunnel = ngrok.connect(BRIDGE_PORT, "http")
    print("╔══════════════════════════════════════════════════════╗")
    print(f"  ngrok public URL: {tunnel.public_url}")
    print(f"  MySQL target:     {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
    print("  Paste the URL above to Claude, then press Ctrl+C to stop.")
    print("╚══════════════════════════════════════════════════════╝")
    HTTPServer(("0.0.0.0", BRIDGE_PORT), Handler).serve_forever()
