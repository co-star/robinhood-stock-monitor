import http.server
import socketserver
import json
import os
import time
import urllib.request
import urllib.parse
import threading
import ssl
from scanner import run_scan, LATEST_SCAN_FILE, BASE_DIR

PORT = 8080

class MonitorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path.startswith('/api/scan-data'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if os.path.exists(LATEST_SCAN_FILE):
                with open(LATEST_SCAN_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": "No scan data available"}).encode('utf-8'))
            return
            
        elif path.startswith('/api/trigger-scan'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            try:
                res = run_scan()
                self.wfile.write(json.dumps({"status": "success", "result": res}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return
            
        elif path.startswith('/api/wallet-positions'):
            query = urllib.parse.parse_qs(parsed.query)
            wallet = query.get("wallet", ["0x1e49fb8a44a7a82327aab531cad10e4796d63f39"])[0].strip()
            
            target_url = "https://interface.gateway.uniswap.org/v2/data.v1.DataApiService/ListPositions"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
                "Origin": "https://app.uniswap.org",
                "Referer": "https://app.uniswap.org/"
            }
            
            # Match user provided official Uniswap payload
            payload = {
                "address": wallet,
                "chainIds": [1,130,8453,42161,4663,4217,143,137,196,10,56,43114,59144,480,324,4326,1868,7777777,42220,81457],
                "protocolVersions": ["PROTOCOL_VERSION_V4","PROTOCOL_VERSION_V3","PROTOCOL_VERSION_V2"],
                "positionStatuses": ["POSITION_STATUS_IN_RANGE","POSITION_STATUS_OUT_OF_RANGE"],
                "pageSize": 50,
                "includeHidden": True
            }
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            try:
                req = urllib.request.Request(
                    target_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
                    res_data = resp.read().decode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(res_data.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                err_resp = json.dumps({"error": str(e), "positions": []})
                self.wfile.write(err_resp.encode("utf-8"))
            return
            
        # Serve static files from web/ directory
        req_path = self.path.split('?')[0]
        if req_path == '/' or req_path == '/index.html':
            target_path = os.path.join(BASE_DIR, 'web', 'index.html')
        else:
            rel_path = req_path.lstrip('/')
            target_path = os.path.join(BASE_DIR, 'web', rel_path)
            
        if os.path.exists(target_path) and os.path.isfile(target_path):
            self.send_response(200)
            if target_path.endswith('.html'):
                self.send_header('Content-Type', 'text/html; charset=utf-8')
            elif target_path.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            elif target_path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            with open(target_path, 'rb') as f:
                self.wfile.write(f.read())
            return
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def periodic_scan(interval_seconds=600):
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Automatic 10-minute scan running...")
            run_scan()
        except Exception as e:
            print(f"Periodic scan error: {e}")
        time.sleep(interval_seconds)

def start_server():
    if not os.path.exists(LATEST_SCAN_FILE):
        print("Initial data file missing, executing scan now...")
        run_scan()
        
    scan_thread = threading.Thread(target=periodic_scan, daemon=True)
    scan_thread.start()
    
    with socketserver.TCPServer(("", PORT), MonitorHandler) as httpd:
        print(f"Monitor web service started at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
