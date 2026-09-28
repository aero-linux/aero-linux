import http.server
import json
import os
import socketserver
import time
from typing import Dict, Any


MOCK_SCHEMAS = {
    "users": [
        {"id": 1, "name": "Ronit Gupta", "role": "Systems Engineer", "status": "active"},
        {"id": 2, "name": "Alex Chen", "role": "Backend Developer", "status": "active"},
        {"id": 3, "name": "Sarah Connor", "role": "Security Researcher", "status": "idle"},
    ],
    "products": [
        {"id": 101, "name": "Aero Workstation", "price": 1499.00, "in_stock": True},
        {"id": 102, "name": "NVMe Gen4 SSD 2TB", "price": 189.99, "in_stock": True},
        {"id": 103, "name": "Mechanical Keyboard (JetBrains)", "price": 129.50, "in_stock": False},
    ],
    "metrics": {
        "status": "healthy",
        "uptime_seconds": 128450,
        "load_average": [0.42, 0.35, 0.28],
        "active_connections": 1420,
    },
}


class AeroMockHandler(http.server.BaseHTTPRequestHandler):
    delay_sec = 0.0

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.delay_sec > 0:
            time.sleep(self.delay_sec)

        path = self.path.strip("/")
        
        # If serving a local json file
        if os.path.exists(path) and path.endswith(".json"):
            try:
                with open(path) as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
                return
            except Exception:
                pass

        if path in MOCK_SCHEMAS:
            data = MOCK_SCHEMAS[path]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
        elif path == "" or path == "api":
            catalog = {
                "message": "⚡ Aero Local Mock REST API Server",
                "endpoints": [f"/api/{k}" for k in MOCK_SCHEMAS.keys()] + [f"/{k}" for k in MOCK_SCHEMAS.keys()],
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(catalog, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Endpoint '/{path}' not found in mock schema."}).encode("utf-8"))


def run_mock_server(port: int = 4000, delay_ms: int = 0):
    AeroMockHandler.delay_sec = delay_ms / 1000.0
    server = socketserver.TCPServer(("0.0.0.0", port), AeroMockHandler)
    print(f"\n⚡ Aero Mock REST API Server running at:")
    print(f" • Root:      http://localhost:{port}")
    print(f" • Users:     http://localhost:{port}/users")
    print(f" • Products:  http://localhost:{port}/products")
    print(f" • Metrics:   http://localhost:{port}/metrics")
    if delay_ms > 0:
        print(f" • Simulated Latency: {delay_ms} ms")
    print(f" • Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Mock Server...")
        server.server_close()
