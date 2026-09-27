import subprocess
import shutil


def check_sdk_environment():
    print("⚡ \033[1;36mAERO DEVELOPER SDK & RUNTIME AUDIT\033[0m")
    print("═" * 55)

    tools = [
        ("Node.js", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("TypeScript", ["tsc", "--version"]),
        ("Python 3", ["python3", "--version"]),
        ("GCC / C Compiler", ["gcc", "--version"]),
        ("Clang", ["clang", "--version"]),
        ("Rust (rustc)", ["rustc", "--version"]),
        ("Cargo", ["cargo", "--version"]),
        ("Go", ["go", "version"]),
        ("Java (OpenJDK)", ["java", "-version"]),
        ("Docker", ["docker", "--version"]),
        ("Git", ["git", "--version"]),
        ("Ollama (Local AI)", ["ollama", "--version"]),
    ]

    for name, cmd in tools:
        executable = cmd[0]
        if shutil.which(executable):
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
                output = res.stdout.strip() or res.stderr.strip()
                version_line = output.split("\n")[0] if output else "Installed"
                print(f"  ✅ \033[1m{name:<18}\033[0m ➔ \033[32m{version_line}\033[0m")
            except Exception:
                print(f"  ✅ \033[1m{name:<18}\033[0m ➔ Installed")
        else:
            print(f"  ⚪ \033[1m{name:<18}\033[0m ➔ \033[90mNot Installed (Install with: aero dev or aero pkg)\033[0m")
    print()
