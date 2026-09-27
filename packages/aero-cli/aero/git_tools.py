import subprocess
import os
import shutil


def check_git_status():
    print("🐙 \033[1;36mAERO GIT WORKSPACE INSPECTOR\033[0m")
    print("═" * 55)

    if not os.path.exists(".git"):
        print("ℹ️ Current directory is not a Git repository.")
        return

    # Current branch & status
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
