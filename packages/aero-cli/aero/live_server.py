import http.server
import json
import os
import socketserver
import time
from typing import Dict, Any

from aero.thermals import get_temperatures
from aero.battery import get_battery_health
from aero.memory import get_memory_stats
from aero.power import get_current_profile


HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚡ Aero Linux — Live Telemetry Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'JetBrains Mono', -apple-system, monospace; }
  body { background: #08090d; color: #f8fafc; padding: 25px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 15px; margin-bottom: 25px; }
  .logo { font-size: 22px; font-weight: 800; color: #00f2fe; }
  .status-badge { background: rgba(52, 211, 153, 0.1); color: #34d399; border: 1px solid #34d399; padding: 4px 12px; border-radius: 12px; font-size: 12px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
  .card { background: #0f131c; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; }
  .card-title { font-size: 14px; color: #94a3b8; margin-bottom: 12px; font-weight: 700; }
  .metric-big { font-size: 28px; font-weight: 800; color: #00f2fe; margin-bottom: 4px; }
  .metric-sub { font-size: 12px; color: #64748b; }
  .green { color: #34d399; }
  .cyan { color: #00f2fe; }
  .yellow { color: #fbbf24; }
  .bar-bg { width: 100%; height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; margin-top: 10px; }
  .bar-fill { height: 100%; background: linear-gradient(90deg, #00f2fe, #4facfe); width: 0%; transition: width 0.5s ease; }
</style>
</head>
<body>
  <div class="header">
    <div class="logo">⚡ Aero Linux Live Telemetry</div>
    <div class="status-badge" id="live-indicator">🟢 CONNECTED (1s Polling)</div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-title">🧠 MEMORY USAGE</div>
      <div class="metric-big" id="ram-used">-- MB</div>
      <div class="metric-sub" id="ram-total">Total: -- MB</div>
      <div class="bar-bg"><div class="bar-fill" id="ram-bar"></div></div>
    </div>
    <div class="card">
      <div class="card-title">🚀 IN-MEMORY zRAM (ZSTD)</div>
      <div class="metric-big green" id="zram-used">-- MB</div>
      <div class="metric-sub" id="zram-total">Device: /dev/zram0</div>
      <div class="bar-bg"><div class="bar-fill" id="zram-bar" style="background:#34d399;"></div></div>
    </div>
    <div class="card">
      <div class="card-title">🌡️ CPU TEMPERATURE</div>
      <div class="metric-big yellow" id="cpu-temp">-- °C</div>
      <div class="metric-sub" id="cpu-governor">Governor: powersave</div>
    </div>
    <div class="card">
      <div class="card-title">🔋 BATTERY HEALTH</div>
      <div class="metric-big" id="bat-pct">-- %</div>
      <div class="metric-sub" id="bat-health">Threshold: 80% Active</div>
    </div>
  </div>

  <script>
    async function updateStats() {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        document.getElementById('ram-used').innerText = `${data.memory.used_mb} MB`;
        document.getElementById('ram-total').innerText = `Total: ${data.memory.total_mb} MB (${data.memory.percent_used}%)`;
        document.getElementById('ram-bar').style.width = `${data.memory.percent_used}%`;

        document.getElementById('zram-used').innerText = `${data.memory.zram_used_mb} MB`;
        document.getElementById('zram-total').innerText = `Total zRAM: ${data.memory.zram_total_mb} MB`;
        document.getElementById('zram-bar').style.width = `${data.memory.zram_percent}%`;

        document.getElementById('cpu-temp').innerText = `${data.thermals.cpu || '51.0'} °C`;
        document.getElementById('bat-pct').innerText = `${data.battery.percentage}%`;
        document.getElementById('bat-health').innerText = `Status: ${data.battery.status} | Health: ${data.battery.health_pct}%`;
      } catch (e) {
        document.getElementById('live-indicator').innerText = '🔴 DISCONNECTED';
        document.getElementById('live-indicator').style.color = '#f87171';
      }
    }
    setInterval(updateStats, 1000);
    updateStats();
  </script>
</body>
</html>
"""


class AeroTelemetryHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress console log clutter

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
        elif self.path == "/api/stats":
            mem = get_memory_stats()
            therms = get_temperatures()
            bat = get_battery_health()
            profile = get_current_profile()
            
            payload = {
                "timestamp": time.time(),
                "memory": mem,
                "thermals": therms,
                "battery": bat,
                "profile": profile,
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run_live_dashboard(port: int = 8080):
    server = socketserver.TCPServer(("0.0.0.0", port), AeroTelemetryHandler)
    print(f"\n⚡ Aero Live Web Dashboard running at:")
    print(f" • Local:   http://localhost:{port}")
    print(f" • Network: http://0.0.0.0:{port}")
    print(f" • Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Live Dashboard server...")
        server.server_close()
