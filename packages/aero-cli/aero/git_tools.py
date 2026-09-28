import subprocess
import os
import shutil


def check_git_status():
    print("🐙 \033[1;36mAERO GIT WORKSPACE INSPECTOR\033[0m")
    print("═" * 55)

    if not os.path.exists(".git"):
        print("ℹ️ Current directory is not a Git repository.")
        return

    try:
        branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.strip()
        last_commit = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True).stdout.strip()

        print(f" • Active Branch: \033[1;33m{branch}\033[0m")
        print(f" • Latest Commit: \033[1;36m{last_commit}\033[0m")
        
        if status:
            print("\nUncommitted Changes:")
            for line in status.split("\n"):
                print(f"   {line}")
        else:
            print("\n✅ Working tree is completely clean.")
    except Exception as e:
        print(f"Git error: {e}")
    print()


def clean_merged_branches():
    print("🧹 Cleaning merged local Git branches...")
    try:
        cmd = "git branch --merged | grep -v '\\*' | grep -v 'main' | grep -v 'master' | xargs -r git branch -d"
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Stale merged branches pruned.")
    except Exception as e:
        print(f"Branch cleanup: {e}")


def show_git_graph(limit: int = 15):
    if not os.path.exists(".git"):
        print("ℹ️ Not a git repository.")
        return
    print("\n🌲 \033[1;36mAERO GIT BRANCH TOPOLOGY GRAPH\033[0m")
    print("═" * 55)
    try:
        cmd = [
            "git", "log", "--graph", "--abbrev-commit", "--decorate",
            "--format=format:%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)",
            f"-n{limit}", "--all"
        ]
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error rendering git graph: {e}")
    print("═" * 55 + "\n")


def show_git_churn():
    if not os.path.exists(".git"):
        print("ℹ️ Not a git repository.")
        return
    print("\n🔥 \033[1;36mAERO GIT CODE CHURN (Top Changed Files)\033[0m")
    print("═" * 55)
    try:
        cmd = "git log --name-only --format='' -n 50 | sort | grep -v '^$' | uniq -c | sort -rn | head -n 10"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.stdout.strip():
            for line in res.stdout.strip().split("\n"):
                print(f"   {line}")
        else:
            print("   (No commit churn history found)")
    except Exception as e:
        print(f"Error: {e}")
    print("═" * 55 + "\n")
