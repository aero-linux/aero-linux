# Fish completion for Aero Linux CLI (aero)

set -l aero_commands doctor memory power ai vault dev net store repair git ssh ssl firewall speed disk sync startup services flasher logs font ports shortcuts notes color screenshot monitor updater wifi bluetooth audio displays gamehub phone security benchmark clean about layout zoom oom wallpaper shell calc diff qr archive sandbox tunnel markdown gpu cron crypto db env mock regex deps search turbomount tiling recorder accent appimage json jwt http ping dig trace thermals battery trash clipboard

complete -c aero -f
complete -c aero -n "not __fish_seen_subcommand_from $aero_commands" -a "$aero_commands"

# Subcommand completions
complete -c aero -n "__fish_seen_subcommand_from power" -a "battery balanced boost gaming --set --threshold"
complete -c aero -n "__fish_seen_subcommand_from ai" -a "init status pull run calc bench qwen2.5-coder:7b deepseek-r1:8b llama3.2:3b codellama:7b"
complete -c aero -n "__fish_seen_subcommand_from vault" -a "set get delete list export"
complete -c aero -n "__fish_seen_subcommand_from dev" -a "setup list run node rust python go docker c"
complete -c aero -n "__fish_seen_subcommand_from store" -a "install search list remove vscode brave docker postman dbeaver obsidian neovim discord lazygit gh btop insomnia"
complete -c aero -n "__fish_seen_subcommand_from theme" -a "list set auto cyber-cyan obsidian-purple matrix-green solarized-amber gruvbox nord-frost"
complete -c aero -n "__fish_seen_subcommand_from layout" -a "windows tiling"
complete -c aero -n "__fish_seen_subcommand_from zoom" -a "set in out reset 1.0 1.25 1.5 2.0"
complete -c aero -n "__fish_seen_subcommand_from gpu" -a "integrated hybrid dedicated status"
complete -c aero -n "__fish_seen_subcommand_from archive" -a "compress extract list"
complete -c aero -n "__fish_seen_subcommand_from tiling" -a "start stop status"
