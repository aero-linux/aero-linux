def list_keybinds():
    shortcuts = [
        ("Super + Return", "Open Alacritty Terminal"),
        ("Super + D", "Open Application Launcher (Wofi / Rofi)"),
        ("Super + Shift + Q", "Kill Focused Window"),
        ("Super + 1-9", "Switch to Workspace 1-9"),
        ("Super + Shift + 1-9", "Move Focused Window to Workspace 1-9"),
        ("Super + F", "Toggle Fullscreen Mode"),
        ("Super + V", "Toggle Floating Window"),
        ("Super + Shift + E", "Aero Power Menu (Lock, Suspend, Reboot, Shutdown)"),
        ("Super + Space", "Toggle Tiling Split Direction (Horizontal / Vertical)"),
        ("Super + ?", "Show this Aero Hotkey Cheatsheet"),
    ]

    aero_cli_shortcuts = [
        ("ai <model>", "Quick run local AI prompt (e.g. 'ai deepseek-r1')"),
        ("doc", "Run system diagnostics ('aero doctor')"),
        ("opt", "Compact zRAM memory & drop pagecaches ('aero memory --optimize')"),
        ("bat", "Switch to quiet power-saving governor ('aero power battery')"),
        ("boost", "Switch to high-performance boost governor ('aero power boost')"),
        ("game", "Switch to max GPU/CPU performance governor ('aero power gaming')"),
    ]

    print("⚡ \033[1;36mAERO DESKTOP KEYBOARD SHORTCUTS\033[0m (Sway / Wayland)")
    print("═" * 65)
    for key, action in shortcuts:
        print(f"  \033[1;33m{key:<22}\033[0m ➔  {action}")

    print("\n⚡ \033[1;36mSHELL ALIASES & QUICK COMMANDS\033[0m")
    print("═" * 65)
    for cmd, desc in aero_cli_shortcuts:
        print(f"  \033[1;32m{cmd:<22}\033[0m ➔  {desc}")
    print()
