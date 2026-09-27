import sys
import subprocess


def run_aero_shell():
    print("⚡ \033[1;36mWelcome to Aero Linux Developer Shell\033[0m")
    print("Type 'help' for available commands or 'exit' to quit.\n")

    while True:
        try:
            cmd = input("\033[1;36maero\033[0m \033[33m❯\033[0m ").strip()
            if not cmd:
                continue

            if cmd in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
            elif cmd in ["help", "?"]:
                print("Commands: doctor, power, memory, ai, dev, pkg, snapshot, net, benchmark, gamemode, port, docker, env, keys, security")
            else:
                args = cmd.split()
                subprocess.run(["aero"] + args)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting shell.")
            break
