# Bash completion for Aero Linux CLI (aero)
# Supported: all 50+ subcommands, options, and arguments

_aero_completions() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="doctor memory power ai vault dev net store repair git ssh ssl firewall speed disk sync startup services flasher logs font ports shortcuts notes color screenshot monitor updater wifi bluetooth audio displays gamehub phone security benchmark clean about layout zoom oom wallpaper shell calc diff qr archive sandbox tunnel markdown gpu cron crypto db env mock regex deps search turbomount tiling recorder accent appimage json jwt http ping dig trace thermals battery trash clipboard"

    if [ "$COMP_CWORD" -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
        return 0
    fi

    case "${prev}" in
        power)
            COMPREPLY=( $(compgen -W "battery balanced boost gaming --set --threshold" -- "${cur}") )
            return 0
            ;;
        ai)
            COMPREPLY=( $(compgen -W "init status pull run calc bench qwen2.5-coder:7b deepseek-r1:8b llama3.2:3b codellama:7b" -- "${cur}") )
            return 0
            ;;
        vault)
            COMPREPLY=( $(compgen -W "set get delete list export" -- "${cur}") )
            return 0
            ;;
        dev)
            COMPREPLY=( $(compgen -W "setup list run node rust python go docker c" -- "${cur}") )
            return 0
            ;;
        net)
            COMPREPLY=( $(compgen -W "bbr dns ping trace dig ports cloudflare google" -- "${cur}") )
            return 0
            ;;
        store)
            COMPREPLY=( $(compgen -W "install search list remove vscode brave docker postman dbeaver obsidian neovim discord lazygit gh btop insomnia" -- "${cur}") )
            return 0
            ;;
        git)
            COMPREPLY=( $(compgen -W "scan sync status" -- "${cur}") )
            return 0
            ;;
        theme)
            COMPREPLY=( $(compgen -W "list set auto cyber-cyan obsidian-purple matrix-green solarized-amber gruvbox nord-frost" -- "${cur}") )
            return 0
            ;;
        layout)
            COMPREPLY=( $(compgen -W "windows tiling" -- "${cur}") )
            return 0
            ;;
        zoom)
            COMPREPLY=( $(compgen -W "set in out reset 1.0 1.25 1.5 2.0" -- "${cur}") )
            return 0
            ;;
        gpu)
            COMPREPLY=( $(compgen -W "integrated hybrid dedicated status" -- "${cur}") )
            return 0
            ;;
        archive)
            COMPREPLY=( $(compgen -W "compress extract list" -- "${cur}") )
            return 0
            ;;
        tiling)
            COMPREPLY=( $(compgen -W "start stop status" -- "${cur}") )
            return 0
            ;;
        *)
            ;;
    esac
}

complete -F _aero_completions aero
