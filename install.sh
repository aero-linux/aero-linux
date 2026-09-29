#!/usr/bin/env bash
# ⚡ Aero Linux — 1-Command Universal Installer
# Installs the Aero CLI, GTK3 Control Center, and Desktop configs system-wide.

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "    ___    ______ ____  ____     __    _____   __  ___  __  __"
echo "   /   |  / ____// __ \/ __ \   / /   /  _/ | / / / / / / |/ /"
echo "  / /| | / __/  / /_/ / / / /  / /    / / |  \| / / / / /|_/ / "
echo " / ___ |/ /___ / _, _/ /_/ /  / /____/ /  | \  / /_/ / /  / /  "
echo "/_/  |_/_____//_/ |_|\____/  /_____/___/  |_|\_/\____/_/  /_/   "
echo -e "${NC}"
echo -e "${CYAN}⚡ Aero Linux 1.0-Edge — Universal System Installer${NC}"
echo -e "${YELLOW}──────────────────────────────────────────────────────────────────────────${NC}"

# Detect installation directory
INSTALL_DIR="${HOME}/.local/share/aero-linux"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${INSTALL_DIR}"
mkdir -p "${BIN_DIR}"
mkdir -p "${HOME}/.local/share/applications"

# Check if installing from local repo or cloning from GitHub
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

if [ -d "${REPO_DIR}/packages/aero-cli" ]; then
    echo -e "${GREEN}• Copying Aero packages from local repository...${NC}"
    cp -r "${REPO_DIR}/packages" "${INSTALL_DIR}/"
    cp -r "${REPO_DIR}/desktop" "${INSTALL_DIR}/" 2>/dev/null || true
    cp -r "${REPO_DIR}/build" "${INSTALL_DIR}/" 2>/dev/null || true
else
    echo -e "${GREEN}• Downloading latest Aero Linux core packages from GitHub...${NC}"
    if command -v git >/dev/null 2>&1; then
        rm -rf "${INSTALL_DIR}/repo"
        git clone --depth 1 https://github.com/ronitgupta138/aero-linux.git "${INSTALL_DIR}/repo"
        cp -r "${INSTALL_DIR}/repo/packages" "${INSTALL_DIR}/"
        cp -r "${INSTALL_DIR}/repo/desktop" "${INSTALL_DIR}/" 2>/dev/null || true
        cp -r "${INSTALL_DIR}/repo/build" "${INSTALL_DIR}/" 2>/dev/null || true
        rm -rf "${INSTALL_DIR}/repo"
    else
        echo -e "${RED}❌ Git is required to clone Aero Linux. Please install git.${NC}"
        exit 1
    fi
fi

# Create global executable wrapper for aero CLI
echo -e "${GREEN}• Installing global 'aero' command into ${BIN_DIR}/aero...${NC}"
cat << 'EOF' > "${BIN_DIR}/aero"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-cli"
export PYTHONPATH="${AERO_HOME}:${PYTHONPATH}"
exec python3 "${AERO_HOME}/bin/aero" "$@"
EOF
chmod +x "${BIN_DIR}/aero"

# Create global executable wrapper for aero-welcome GUI
cat << 'EOF' > "${BIN_DIR}/aero-welcome"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-welcome" "$@"
EOF
chmod +x "${BIN_DIR}/aero-welcome"

# Create global executable wrapper for aero-quick-settings GUI
cat << 'EOF' > "${BIN_DIR}/aero-quick-settings"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-quick-settings" "$@"
EOF
chmod +x "${BIN_DIR}/aero-quick-settings"

# Create global executable wrapper for aero-monitor GUI
cat << 'EOF' > "${BIN_DIR}/aero-monitor"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-monitor" "$@"
EOF
chmod +x "${BIN_DIR}/aero-monitor"

# Create global executable wrapper for aero-updater GUI
cat << 'EOF' > "${BIN_DIR}/aero-updater"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-updater" "$@"
EOF
chmod +x "${BIN_DIR}/aero-updater"

# Create global executable wrapper for aero-wifi GUI
cat << 'EOF' > "${BIN_DIR}/aero-wifi"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-wifi" "$@"
EOF
chmod +x "${BIN_DIR}/aero-wifi"

# Create global executable wrapper for aero-snapshot-gui
cat << 'EOF' > "${BIN_DIR}/aero-snapshot-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-snapshot-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-snapshot-gui"

# Create global executable wrapper for aero-bluetooth GUI
cat << 'EOF' > "${BIN_DIR}/aero-bluetooth"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-bluetooth" "$@"
EOF
chmod +x "${BIN_DIR}/aero-bluetooth"

# Create global executable wrapper for aero-audio GUI
cat << 'EOF' > "${BIN_DIR}/aero-audio"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-audio" "$@"
EOF
chmod +x "${BIN_DIR}/aero-audio"

# Create global executable wrapper for aero-displays GUI
cat << 'EOF' > "${BIN_DIR}/aero-displays"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-displays" "$@"
EOF
chmod +x "${BIN_DIR}/aero-displays"

# Create global executable wrapper for aero-spotlight GUI
cat << 'EOF' > "${BIN_DIR}/aero-spotlight"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-spotlight" "$@"
EOF
chmod +x "${BIN_DIR}/aero-spotlight"

# Create global executable wrapper for aero-gamehub GUI
cat << 'EOF' > "${BIN_DIR}/aero-gamehub"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-gamehub" "$@"
EOF
chmod +x "${BIN_DIR}/aero-gamehub"

# Create global executable wrapper for aero-connect-gui
cat << 'EOF' > "${BIN_DIR}/aero-connect-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-connect-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-connect-gui"

# Create global executable wrapper for aero-power-gui
cat << 'EOF' > "${BIN_DIR}/aero-power-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-power-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-power-gui"

# Create global executable wrapper for aero-nightlight-gui
cat << 'EOF' > "${BIN_DIR}/aero-nightlight-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-nightlight-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-nightlight-gui"

# Create global executable wrapper for aero-theme-gui
cat << 'EOF' > "${BIN_DIR}/aero-theme-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-theme-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-theme-gui"

# Create global executable wrapper for aero-cleaner-gui
cat << 'EOF' > "${BIN_DIR}/aero-cleaner-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-cleaner-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-cleaner-gui"

# Create global executable wrapper for aero-vault-gui
cat << 'EOF' > "${BIN_DIR}/aero-vault-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-vault-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-vault-gui"

# Create global executable wrapper for aero-about-gui
cat << 'EOF' > "${BIN_DIR}/aero-about"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-about-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-about"

# Create global executable wrapper for aero-screenshot-gui
cat << 'EOF' > "${BIN_DIR}/aero-screenshot"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-screenshot-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-screenshot"

# Create global executable wrapper for aero-repair-gui
cat << 'EOF' > "${BIN_DIR}/aero-repair-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-repair-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-repair-gui"

# Create global executable wrapper for aero-notes-gui
cat << 'EOF' > "${BIN_DIR}/aero-notes"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-notes-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-notes"

# Create global executable wrapper for aero-color-gui
cat << 'EOF' > "${BIN_DIR}/aero-color"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-color-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-color"

# Create global executable wrapper for aero-font-gui
cat << 'EOF' > "${BIN_DIR}/aero-font-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-font-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-font-gui"

# Create global executable wrapper for aero-ports-gui
cat << 'EOF' > "${BIN_DIR}/aero-ports-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-ports-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-ports-gui"

# Create global executable wrapper for aero-shortcuts-gui
cat << 'EOF' > "${BIN_DIR}/aero-shortcuts-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-shortcuts-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-shortcuts-gui"

# Create global executable wrapper for aero-flasher-gui
cat << 'EOF' > "${BIN_DIR}/aero-flasher-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-flasher-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-flasher-gui"

# Create global executable wrapper for aero-logs-gui
cat << 'EOF' > "${BIN_DIR}/aero-logs-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-logs-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-logs-gui"

# Create global executable wrapper for aero-services-gui
cat << 'EOF' > "${BIN_DIR}/aero-services-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-services-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-services-gui"

# Create global executable wrapper for aero-startup-gui
cat << 'EOF' > "${BIN_DIR}/aero-startup-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-startup-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-startup-gui"

# Create global executable wrapper for aero-sync-gui
cat << 'EOF' > "${BIN_DIR}/aero-sync-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-sync-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-sync-gui"

# Create global executable wrapper for aero-disk-gui
cat << 'EOF' > "${BIN_DIR}/aero-disk-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-disk-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-disk-gui"

# Create global executable wrapper for aero-speed-gui
cat << 'EOF' > "${BIN_DIR}/aero-speed-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-speed-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-speed-gui"

# Create global executable wrapper for aero-git-gui
cat << 'EOF' > "${BIN_DIR}/aero-git-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-git-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-git-gui"

# Create global executable wrapper for aero-firewall-gui
cat << 'EOF' > "${BIN_DIR}/aero-firewall-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-firewall-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-firewall-gui"

# Create global executable wrapper for aero-ssh-gui
cat << 'EOF' > "${BIN_DIR}/aero-ssh-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-ssh-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-ssh-gui"

# Create global executable wrapper for aero-ssl-gui
cat << 'EOF' > "${BIN_DIR}/aero-ssl-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-ssl-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-ssl-gui"

# Create global executable wrapper for aero-ai-gui
cat << 'EOF' > "${BIN_DIR}/aero-ai-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-ai-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-ai-gui"

# Create global executable wrapper for aero-workspaces-gui
cat << 'EOF' > "${BIN_DIR}/aero-workspaces-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-workspaces-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-workspaces-gui"

# Create global executable wrapper for aero-snapshots-gui
cat << 'EOF' > "${BIN_DIR}/aero-snapshots-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-snapshots-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-snapshots-gui"

# Create global executable wrapper for aero-docker-gui
cat << 'EOF' > "${BIN_DIR}/aero-docker-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-docker-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-docker-gui"

# Create global executable wrapper for aero-api-gui
cat << 'EOF' > "${BIN_DIR}/aero-api-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-api-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-api-gui"

# Create global executable wrapper for aero-env-gui
cat << 'EOF' > "${BIN_DIR}/aero-env-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-env-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-env-gui"

# Create global executable wrapper for aero-regex-gui
cat << 'EOF' > "${BIN_DIR}/aero-regex-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-regex-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-regex-gui"

# Create global executable wrapper for aero-db-gui
cat << 'EOF' > "${BIN_DIR}/aero-db-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-db-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-db-gui"

# Create global executable wrapper for aero-cron-gui
cat << 'EOF' > "${BIN_DIR}/aero-cron-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-cron-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-cron-gui"

# Create global executable wrapper for aero-crypto-gui
cat << 'EOF' > "${BIN_DIR}/aero-crypto-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-crypto-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-crypto-gui"

# Create global executable wrapper for aero-mock-gui
cat << 'EOF' > "${BIN_DIR}/aero-mock-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-mock-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-mock-gui"

# Create global executable wrapper for aero-deps-gui
cat << 'EOF' > "${BIN_DIR}/aero-deps-gui"
#!/usr/bin/env bash
AERO_HOME="${HOME}/.local/share/aero-linux/packages/aero-welcome"
exec python3 "${AERO_HOME}/bin/aero-deps-gui" "$@"
EOF
chmod +x "${BIN_DIR}/aero-deps-gui"

# Install Desktop Icon & Man Pages & Nemo File Manager Actions
mkdir -p "${HOME}/.local/share/icons/hicolor/scalable/apps"
mkdir -p "${HOME}/.local/share/man/man1"
mkdir -p "${HOME}/.local/share/nemo/actions"
cp "${INSTALL_DIR}/desktop/icons/aero-logo.svg" "${HOME}/.local/share/icons/hicolor/scalable/apps/aero.svg" 2>/dev/null || true
cp "${INSTALL_DIR}/docs/man/aero.1" "${HOME}/.local/share/man/man1/aero.1" 2>/dev/null || true
cp -r "${INSTALL_DIR}/desktop/configs/nemo-actions/"*.nemo_action "${HOME}/.local/share/nemo/actions/" 2>/dev/null || true

# Register desktop application icon in Start Menu
echo -e "${GREEN}• Creating Start Menu / Desktop Launcher entry...${NC}"
cat << EOF > "${HOME}/.local/share/applications/aero-welcome.desktop"
[Desktop Entry]
Name=Aero Control Center
Comment=Aero Linux Quick Setup & Telemetry GUI
Exec=${BIN_DIR}/aero-welcome
Icon=aero
Terminal=false
Type=Application
Categories=System;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-monitor.desktop"
[Desktop Entry]
Name=Aero System Monitor
Comment=Aero Linux Graphical CPU Waveform & Task Manager
Exec=${BIN_DIR}/aero-monitor
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Monitor;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-updater.desktop"
[Desktop Entry]
Name=Aero Update Manager
Comment=Aero Linux System & Package Updater GUI
Exec=${BIN_DIR}/aero-updater
Icon=system-software-update
Terminal=false
Type=Application
Categories=System;PackageManager;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-terminal.desktop"
[Desktop Entry]
Name=Aero Terminal
Comment=Aero Linux High-Performance GPU-Accelerated Terminal
Exec=alacritty -e ${BIN_DIR}/aero doctor
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=System;TerminalEmulator;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-wifi.desktop"
[Desktop Entry]
Name=Aero Wi-Fi Center
Comment=Aero Linux Wireless & Network Manager
Exec=${BIN_DIR}/aero-wifi
Icon=network-wireless
Terminal=false
Type=Application
Categories=System;Settings;Network;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-snapshot.desktop"
[Desktop Entry]
Name=Aero TimeMachine
Comment=Aero Linux System Restore Points & Rollback
Exec=${BIN_DIR}/aero-snapshot-gui
Icon=system-software-update
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-bluetooth.desktop"
[Desktop Entry]
Name=Aero Bluetooth Center
Comment=Aero Linux Bluetooth & Device Pairing Center
Exec=${BIN_DIR}/aero-bluetooth
Icon=bluetooth
Terminal=false
Type=Application
Categories=System;Settings;HardwareSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-audio.desktop"
[Desktop Entry]
Name=Aero Sound Center
Comment=Aero Linux Audio Output Switcher & Mixer
Exec=${BIN_DIR}/aero-audio
Icon=audio-volume-high
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Mixer;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-displays.desktop"
[Desktop Entry]
Name=Aero Displays & Scaling
Comment=Aero Linux Screen Resolution, Refresh Rate & HiDPI Manager
Exec=${BIN_DIR}/aero-displays
Icon=video-display
Terminal=false
Type=Application
Categories=System;Settings;HardwareSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-spotlight.desktop"
[Desktop Entry]
Name=Aero Spotlight
Comment=Aero Linux Universal Raycast Search & Command Palette
Exec=${BIN_DIR}/aero-spotlight
Icon=system-search
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-gamehub.desktop"
[Desktop Entry]
Name=Aero Game Hub
Comment=Aero Linux Proton & GameMode Optimizer
Exec=${BIN_DIR}/aero-gamehub
Icon=applications-games
Terminal=false
Type=Application
Categories=Game;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-connect.desktop"
[Desktop Entry]
Name=Aero Phone Link
Comment=Aero Linux Wireless Drop & Phone Link
Exec=${BIN_DIR}/aero-connect-gui
Icon=phone
Terminal=false
Type=Application
Categories=Network;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-power.desktop"
[Desktop Entry]
Name=Aero Battery & Thermals
Comment=Aero Linux Battery Care, Fan Curves & Power Profiles
Exec=${BIN_DIR}/aero-power-gui
Icon=battery
Terminal=false
Type=Application
Categories=System;Settings;HardwareSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-nightlight.desktop"
[Desktop Entry]
Name=Aero Night Light
Comment=Aero Linux Blue Light & Color Temperature Studio
Exec=${BIN_DIR}/aero-nightlight-gui
Icon=display
Terminal=false
Type=Application
Categories=System;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-theme.desktop"
[Desktop Entry]
Name=Aero Theme Studio
Comment=Aero Linux Themes, Accent Colors & Wallpaper Generator
Exec=${BIN_DIR}/aero-theme-gui
Icon=preferences-desktop-theme
Terminal=false
Type=Application
Categories=System;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-cleaner.desktop"
[Desktop Entry]
Name=Aero System Cleaner
Comment=Aero Linux Disk Cleaner & Cache De-bloater
Exec=${BIN_DIR}/aero-cleaner-gui
Icon=user-trash
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-vault.desktop"
[Desktop Entry]
Name=Aero Developer Vault
Comment=Aero Linux Encrypted Secrets & API Key Vault
Exec=${BIN_DIR}/aero-vault-gui
Icon=dialog-password
Terminal=false
Type=Application
Categories=Development;Security;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-about.desktop"
[Desktop Entry]
Name=About Aero Linux
Comment=Aero Linux System Information & Hardware Specifications
Exec=${BIN_DIR}/aero-about
Icon=help-about
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-screenshot.desktop"
[Desktop Entry]
Name=Aero Screenshot Tool
Comment=Aero Linux Snip & Screen Capture Tool
Exec=${BIN_DIR}/aero-screenshot
Icon=applets-screenshooter
Terminal=false
Type=Application
Categories=Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-repair.desktop"
[Desktop Entry]
Name=Aero Self-Repair Center
Comment=Aero Linux System Health, Package Locks & Network Healer
Exec=${BIN_DIR}/aero-repair-gui
Icon=system-software-update
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-notes.desktop"
[Desktop Entry]
Name=Aero Scratchpad Notes
Comment=Aero Linux Developer Floating Markdown Scratchpad
Exec=${BIN_DIR}/aero-notes
Icon=accessories-text-editor
Terminal=false
Type=Application
Categories=Utility;TextEditor;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-color.desktop"
[Desktop Entry]
Name=Aero Color Picker
Comment=Aero Linux Pixel Color Dropper & HEX/RGB Studio
Exec=${BIN_DIR}/aero-color
Icon=color-picker
Terminal=false
Type=Application
Categories=Graphics;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-font.desktop"
[Desktop Entry]
Name=Aero Typography Studio
Comment=Aero Linux Font Manager & Ligature Previewer
Exec=${BIN_DIR}/aero-font-gui
Icon=font-x-generic
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-ports.desktop"
[Desktop Entry]
Name=Aero Port Inspector
Comment=Aero Linux Dev Server & Listening Port Manager
Exec=${BIN_DIR}/aero-ports-gui
Icon=network-server
Terminal=false
Type=Application
Categories=Development;System;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-shortcuts.desktop"
[Desktop Entry]
Name=Aero Keyboard Shortcuts
Comment=Aero Linux Keyboard Shortcuts & Hotkey Guide
Exec=${BIN_DIR}/aero-shortcuts-gui
Icon=input-keyboard
Terminal=false
Type=Application
Categories=Utility;Help;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-flasher.desktop"
[Desktop Entry]
Name=Aero USB Flasher
Comment=Aero Linux Safe ISO & Live USB Creator
Exec=${BIN_DIR}/aero-flasher-gui
Icon=drive-removable-media
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-logs.desktop"
[Desktop Entry]
Name=Aero System Logs
Comment=Aero Linux Live Journald & Kernel Diagnostic Viewer
Exec=${BIN_DIR}/aero-logs-gui
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Monitor;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-services.desktop"
[Desktop Entry]
Name=Aero Services Manager
Comment=Aero Linux Systemd Daemons & Background Services Manager
Exec=${BIN_DIR}/aero-services-gui
Icon=system-run
Terminal=false
Type=Application
Categories=System;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-startup.desktop"
[Desktop Entry]
Name=Aero Startup Applications
Comment=Aero Linux Login Autostart Programs Manager
Exec=${BIN_DIR}/aero-startup-gui
Icon=system-run
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-sync.desktop"
[Desktop Entry]
Name=Aero Dotfiles Sync
Comment=Aero Linux Configs & Settings Cloud Sync
Exec=${BIN_DIR}/aero-sync-gui
Icon=folder-cloud
Terminal=false
Type=Application
Categories=Utility;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-disk.desktop"
[Desktop Entry]
Name=Aero Disk Visualizer
Comment=Aero Linux Storage & Developer Artifact Cleaner
Exec=${BIN_DIR}/aero-disk-gui
Icon=drive-harddisk
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-speed.desktop"
[Desktop Entry]
Name=Aero Network Speed & Latency
Comment=Aero Linux Latency Profiler & DNS Speed Tester
Exec=${BIN_DIR}/aero-speed-gui
Icon=network-wireless
Terminal=false
Type=Application
Categories=System;Network;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-git.desktop"
[Desktop Entry]
Name=Aero Git Dashboard
Comment=Aero Linux Local Git Workspace & Repository Monitor
Exec=${BIN_DIR}/aero-git-gui
Icon=git
Terminal=false
Type=Application
Categories=Development;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-firewall.desktop"
[Desktop Entry]
Name=Aero Firewall & Shield
Comment=Aero Linux UFW Firewall & Port Rules Studio
Exec=${BIN_DIR}/aero-firewall-gui
Icon=security-high
Terminal=false
Type=Application
Categories=System;Security;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-ssh.desktop"
[Desktop Entry]
Name=Aero SSH & Remote Servers
Comment=Aero Linux SSH Keys Generator & Server Bookmarks
Exec=${BIN_DIR}/aero-ssh-gui
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Network;Development;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-ssl.desktop"
[Desktop Entry]
Name=Aero SSL & Dev Certs
Comment=Aero Linux Local HTTPS SSL/TLS Certificates Studio
Exec=${BIN_DIR}/aero-ssl-gui
Icon=security-medium
Terminal=false
Type=Application
Categories=Development;Security;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-ai.desktop"
[Desktop Entry]
Name=Aero Local AI Studio
Comment=Aero Linux Offline LLM Model Serving & Assistant
Exec=${BIN_DIR}/aero-ai-gui
Icon=system-search
Terminal=false
Type=Application
Categories=Development;ArtificialIntelligence;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-workspaces.desktop"
[Desktop Entry]
Name=Aero Workspaces & Desktops
Comment=Aero Linux Virtual Workspaces & Window Organizer
Exec=${BIN_DIR}/aero-workspaces-gui
Icon=preferences-desktop-workspaces
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-snapshots.desktop"
[Desktop Entry]
Name=Aero TimeMachine Snapshots
Comment=Aero Linux System Restore Points & TimeMachine Backups
Exec=${BIN_DIR}/aero-snapshots-gui
Icon=document-revert
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-docker.desktop"
[Desktop Entry]
Name=Aero Docker & Containers
Comment=Aero Linux Docker Container & Microservices Studio
Exec=${BIN_DIR}/aero-docker-gui
Icon=docker
Terminal=false
Type=Application
Categories=Development;System;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-api.desktop"
[Desktop Entry]
Name=Aero API & HTTP Studio
Comment=Aero Linux REST, GraphQL & HTTP Microservices Studio
Exec=${BIN_DIR}/aero-api-gui
Icon=network-server
Terminal=false
Type=Application
Categories=Development;Network;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-env.desktop"
[Desktop Entry]
Name=Aero Environment Studio
Comment=Aero Linux Project .env & Secrets Studio
Exec=${BIN_DIR}/aero-env-gui
Icon=security-high
Terminal=false
Type=Application
Categories=Development;Settings;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-regex.desktop"
[Desktop Entry]
Name=Aero Regex Studio
Comment=Aero Linux Regular Expression & Pattern Evaluator
Exec=${BIN_DIR}/aero-regex-gui
Icon=text-editor
Terminal=false
Type=Application
Categories=Development;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-db.desktop"
[Desktop Entry]
Name=Aero Database Studio
Comment=Aero Linux SQLite & Database Query Studio
Exec=${BIN_DIR}/aero-db-gui
Icon=server-database
Terminal=false
Type=Application
Categories=Development;Database;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-cron.desktop"
[Desktop Entry]
Name=Aero Scheduled Tasks
Comment=Aero Linux Cron & Scheduled Task Automation Studio
Exec=${BIN_DIR}/aero-cron-gui
Icon=alarm
Terminal=false
Type=Application
Categories=System;Utility;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-crypto.desktop"
[Desktop Entry]
Name=Aero Cryptography & JWT
Comment=Aero Linux JWT Decoder & Hash Calculator Studio
Exec=${BIN_DIR}/aero-crypto-gui
Icon=security-high
Terminal=false
Type=Application
Categories=Development;Security;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-mock.desktop"
[Desktop Entry]
Name=Aero Mock Server & Webhook
Comment=Aero Linux Mock REST API Server & Webhook Studio
Exec=${BIN_DIR}/aero-mock-gui
Icon=network-server
Terminal=false
Type=Application
Categories=Development;Network;GTK;
EOF

cat << EOF > "${HOME}/.local/share/applications/aero-deps.desktop"
[Desktop Entry]
Name=Aero Package & Dependencies Studio
Comment=Aero Linux Package & Shared Library Inspector
Exec=${BIN_DIR}/aero-deps-gui
Icon=system-software-install
Terminal=false
Type=Application
Categories=System;Development;GTK;
EOF

# Ensure ~/.local/bin is in PATH for bash, zsh, fish
for rc in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
    if [ -f "$rc" ] && ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
    fi
done

# Install Fish completions if Fish is installed
if [ -d "${HOME}/.config/fish" ]; then
    mkdir -p "${HOME}/.config/fish/completions"
    cp "${INSTALL_DIR}/build/completions/aero.fish" "${HOME}/.config/fish/completions/" 2>/dev/null || true
fi

echo -e "${YELLOW}──────────────────────────────────────────────────────────────────────────${NC}"
echo -e "${GREEN}✅ Aero Linux successfully installed!${NC}"
echo ""
echo -e "You can now run:"
echo -e "  ${CYAN}aero doctor${NC}       ➔ Check system, CPU, zRAM & GPU status"
echo -e "  ${CYAN}aero monitor${NC}      ➔ Open live interactive hardware dashboard"
echo -e "  ${CYAN}aero temp${NC}         ➔ Check hardware chip thermals"
echo -e "  ${CYAN}aero-welcome${NC}      ➔ Launch the GTK3 Control Center GUI"
echo -e "  ${CYAN}aero layout${NC}       ➔ Switch between Windows & Hacker Tiling modes"
echo ""
echo -e "${YELLOW}Tip: Run 'export PATH=\"\$HOME/.local/bin:\$PATH\"' or restart your terminal.${NC}"
