import http.server
import socketserver
import os
import socket


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_file_server(path: str = ".", port: int = 8080):
    if not os.path.exists(path):
        print(f"❌ Target path '{path}' does not exist.")
        return

    os.chdir(path)
    ip = get_local_ip()

    print(f"⚡ \033[1;36mAERO LOCAL NETWORK FILE SERVER\033[0m")
    print("═" * 55)
    print(f" • Serving Directory: \033[1;33m{os.path.abspath('.')}\033[0m")
    print(f" • Local URL:         \033[1;32mhttp://{ip}:{port}\033[0m")
    print(" • Press \033[1mCtrl+C\033[0m to stop the server.\n")

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 File server stopped.")
