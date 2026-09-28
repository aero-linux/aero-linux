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

# Install Desktop Icon & Man Pages
mkdir -p "${HOME}/.local/share/icons/hicolor/scalable/apps"
mkdir -p "${HOME}/.local/share/man/man1"
cp "${INSTALL_DIR}/desktop/icons/aero-logo.svg" "${HOME}/.local/share/icons/hicolor/scalable/apps/aero.svg" 2>/dev/null || true
cp "${INSTALL_DIR}/docs/man/aero.1" "${HOME}/.local/share/man/man1/aero.1" 2>/dev/null || true

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
