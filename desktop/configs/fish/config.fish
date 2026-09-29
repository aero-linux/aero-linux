# Aero Linux Shell Configuration
if status is-interactive
    # Fast Aero Core Aliases
    alias ai="aero ai"
    alias doc="aero doctor"
    alias opt="aero memory --optimize"
    alias flush="aero memory --flush"
    alias bat="aero power battery"
    alias boost="aero power boost"
    alias game="aero power gaming"
    alias ports="aero ports"
    alias bench="aero benchmark"
    alias vault="aero vault"

    # Git shortcuts
    alias gs="git status -sb"
    alias gp="git push"
    alias gl="git log --oneline -n 10"
    alias gd="git diff"

    # GUI Fast Launchers
    alias monitor="aero-monitor"
    alias spot="aero-spotlight"
    alias scratch="aero-notes-gui"

    # Minimal Fast Prompt
    function fish_prompt
        set_color 00f2fe
        echo -n "⚡ aero "
        set_color 4facfe
        echo -n (prompt_pwd)
        set_color f8fafc
        echo -n " ❯ "
    end
end
