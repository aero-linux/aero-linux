import os
import subprocess


def get_git_branch_fast() -> str:
    """Reads git branch directly from .git/HEAD in sub-millisecond time without spawning git."""
    cur = os.getcwd()
    while cur != "/":
        git_dir = os.path.join(cur, ".git")
        if os.path.exists(git_dir):
            if os.path.isfile(git_dir): # git submodule or worktree
                try:
                    with open(git_dir) as f:
                        line = f.read().strip()
                        if line.startswith("gitdir:"):
                            git_dir = os.path.abspath(os.path.join(cur, line.split(":", 1)[1].strip()))
                except Exception:
                    pass
            head_file = os.path.join(git_dir, "HEAD")
            if os.path.exists(head_file):
                try:
                    with open(head_file) as f:
                        ref = f.read().strip()
                        if ref.startswith("ref: refs/heads/"):
                            return ref.replace("ref: refs/heads/", "")
                        return ref[:7] # detached commit sha
                except Exception:
                    pass
            break
        cur = os.path.dirname(cur)
    return ""


def render_prompt(shell: str = "bash") -> str:
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        display_cwd = "~" + cwd[len(home):]
    else:
        display_cwd = cwd

    branch = get_git_branch_fast()
    git_part = f" \033[1;33m({branch})\033[0m" if branch else ""

    if shell == "fish":
        prompt_str = f"\033[1;36m⚡ aero\033[0m \033[1;34m{display_cwd}\033[0m{git_part} \033[1;32m❯\033[0m "
    else:
        # Bash / Zsh compatible ANSI format
        prompt_str = f"\\[\\033[1;36m\\]⚡ aero\\[\\033[0m\\] \\[\\033[1;34m\\]{display_cwd}\\[\\033[0m\\]{git_part} \\[\\033[1;32m\\]❯\\[\\033[0m\\] "

    return prompt_str
