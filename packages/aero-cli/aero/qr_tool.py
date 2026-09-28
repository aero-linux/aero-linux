import shutil
import subprocess
import urllib.parse


def render_qr_terminal(payload: str):
    print(f"\n📱 \033[1;36mAERO TERMINAL QR CODE GENERATOR\033[0m")
    print("═" * 54)
    print(f" • Payload: \033[1;32m{payload}\033[0m\n")

    if shutil.which("qrencode"):
        try:
            subprocess.run(["qrencode", "-t", "UTF8", payload])
            print("\nScan with your smartphone camera to connect / open.")
            print("═" * 54 + "\n")
            return
        except Exception:
            pass

    # Zero-dependency web/terminal rendering via ASCII helper or ANSI fallback
    print(f"Quick Open URL: https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(payload)}")
    print("═" * 54 + "\n")


def generate_wifi_qr(ssid: str, password: str, auth_type: str = "WPA"):
    wifi_str = f"WIFI:S:{ssid};T:{auth_type};P:{password};;"
    render_qr_terminal(wifi_str)
