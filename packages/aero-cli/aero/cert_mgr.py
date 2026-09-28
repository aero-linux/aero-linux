import os
import shutil
import subprocess


def generate_dev_certificate(domain: str = "localhost", out_dir: str = ".") -> bool:
    if not shutil.which("openssl"):
        print("❌ OpenSSL is required to generate SSL certificates.")
        return False

    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    key_path = os.path.join(out_dir, f"{domain}.key")
    crt_path = os.path.join(out_dir, f"{domain}.crt")

    print(f"\n🔒 \033[1;36mGENERATING LOCAL DEVELOPER SSL/TLS CERTIFICATE\033[0m")
    print("═" * 56)
    print(f" • Domain: {domain} (SANs: localhost, 127.0.0.1)")
    print(f" • Output Key:  {key_path}")
    print(f" • Output Cert: {crt_path}")

    openssl_cnf = f"""
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
C = US
ST = Dev
L = Local
O = Aero Dev CA
CN = {domain}

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = {domain}
DNS.2 = *.localhost
IP.1 = 127.0.0.1
IP.2 = ::1
"""
    cnf_file = os.path.join(out_dir, "temp_openssl.cnf")
    try:
        with open(cnf_file, "w") as f:
            f.write(openssl_cnf)

        cmd = [
            "openssl", "req", "-x509", "-nodes", "-days", "365",
            "-newkey", "rsa:2048",
            "-keyout", key_path,
            "-out", crt_path,
            "-config", cnf_file,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(cnf_file):
            os.remove(cnf_file)

        if res.returncode == 0:
            print("\n\033[1;32m✔ SSL Certificate & Private Key generated successfully!\033[0m")
            print("Usage in Node.js/FastAPI/Nginx:")
            print(f"  Key:  {key_path}")
            print(f"  Cert: {crt_path}")
            print("═" * 56 + "\n")
            return True
        else:
            print(f"❌ OpenSSL error: {res.stderr}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        if os.path.exists(cnf_file):
            os.remove(cnf_file)
        return False
