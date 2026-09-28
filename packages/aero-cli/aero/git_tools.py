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


def scan_local_git_workspaces(scan_roots=None):
    """Scan and list all local git repositories and their branch/status/unpushed info."""
    if scan_roots is None:
        scan_roots = [os.path.expanduser("~")]
        area51 = "/media/ronit138/Area 51"
        if os.path.exists(area51):
            scan_roots.append(area51)

    repos = []
    for root_dir in scan_roots:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            if "/." in root and not root.endswith("/.") and ".config" not in root:
                continue
            if root.count(os.sep) - root_dir.count(os.sep) > 3:
                dirs[:] = []
                continue
            if ".git" in dirs:
                dirs.remove(".git")
                repo_path = root
                try:
                    res_b = subprocess.run(["git", "-C", repo_path, "branch", "--show-current"], capture_output=True, text=True)
                    branch = res_b.stdout.strip() or "HEAD (detached)"

                    res_s = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"], capture_output=True, text=True)
                    modified_count = len([line for line in res_s.stdout.splitlines() if line.strip()])
                    is_clean = (modified_count == 0)

                    ahead = 0
                    res_a = subprocess.run(["git", "-C", repo_path, "rev-list", "--count", "@{u}..HEAD"], capture_output=True, text=True)
                    if res_a.returncode == 0 and res_a.stdout.strip().isdigit():
                        ahead = int(res_a.stdout.strip())

                    repos.append({
                        "name": os.path.basename(repo_path),
                        "path": repo_path,
                        "branch": branch,
                        "is_clean": is_clean,
                        "modified_count": modified_count,
                        "ahead": ahead
                    })
                except Exception:
                    pass
    return repos


def print_git_workspaces(scan_roots=None):
    print("\n🌿 \033[1;36mAERO MULTI-REPOSITORY GIT SCANNER\033[0m")
    print("═" * 65)
    repos = scan_local_git_workspaces(scan_roots)
    if not repos:
        print("  (No git repositories found in scanned roots)")
        print("═" * 65 + "\n")
        return repos

    for r in repos:
        clean_tag = "\033[1;32m✔ CLEAN\033[0m" if r["is_clean"] else f"\033[1;33m● DIRTY ({r['modified_count']} modified)\033[0m"
        ahead_tag = f" \033[1;34m[▲ {r['ahead']} unpushed]\033[0m" if r["ahead"] > 0 else ""
        print(f" 📂 \033[1;37m{r['name']:<22}\033[0m 🌿 \033[1;35m{r['branch']:<16}\033[0m {clean_tag}{ahead_tag}")
        print(f"    \033[0;90m└─ {r['path']}\033[0m")

    clean_count = sum(1 for r in repos if r["is_clean"])
    dirty_count = len(repos) - clean_count
    print("─" * 65)
    print(f"Total Repositories: \033[1;36m{len(repos)}\033[0m | Clean: \033[1;32m{clean_count}\033[0m | Uncommitted: \033[1;33m{dirty_count}\033[0m")
    print("═" * 65 + "\n")
    return repos

