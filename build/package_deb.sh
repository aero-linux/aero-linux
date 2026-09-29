#!/usr/bin/env bash
# ==============================================================================
# Aero Linux - Automated Debian (.deb) Package Builder
# Packages the entire Aero CLI, 30-app GUI suite, autocompletions & man pages
# ==============================================================================

set -euo pipefail

VERSION="1.4.0"
PKG_NAME="aero-linux"
ARCH="amd64"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
PKG_DIR="${DIST_DIR}/pkg_deb_${PKG_NAME}_${VERSION}"

echo "📦 Building Debian package: ${PKG_NAME}_${VERSION}_${ARCH}.deb..."

rm -rf "${PKG_DIR}"
mkdir -p "${DIST_DIR}"
mkdir -p "${PKG_DIR}/DEBIAN"
mkdir -p "${PKG_DIR}/usr/bin"
mkdir -p "${PKG_DIR}/usr/lib/aero"
mkdir -p "${PKG_DIR}/usr/share/applications"
mkdir -p "${PKG_DIR}/usr/share/man/man1"
mkdir -p "${PKG_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${PKG_DIR}/usr/share/bash-completion/completions"
mkdir -p "${PKG_DIR}/usr/share/fish/vendor_completions.d"
mkdir -p "${PKG_DIR}/usr/share/zsh/vendor-completions"

# 1. DEBIAN Control File
cat << EOF > "${PKG_DIR}/DEBIAN/control"
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: Ronit Gupta <ronitgupta138@gmail.com>
Depends: python3 (>= 3.10), python3-gi, gir1.2-gtk-3.0, python3-setuptools
Recommends: sway, waybar, alacritty, ufw, pipewire, brightnessctl
Description: The Ultra-Lean AI & High-Performance Developer Linux Control Suite
 Complete 30-application Zero-Terminal GTK3 Graphical Management Suite,
 real-time hardware telemetry, dynamic zRAM compaction, local LLM serving,
 and power management engine for Aero Linux.
EOF

# 2. Copy CLI and Welcome Suites to /usr/lib/aero
cp -r "${ROOT_DIR}/packages/aero-cli" "${PKG_DIR}/usr/lib/aero/"
cp -r "${ROOT_DIR}/packages/aero-welcome" "${PKG_DIR}/usr/lib/aero/"

# 3. Main aero binary wrapper in /usr/bin
cat << 'EOF' > "${PKG_DIR}/usr/bin/aero"
#!/usr/bin/env bash
export PYTHONPATH="/usr/lib/aero/aero-cli:${PYTHONPATH:-}"
exec python3 "/usr/lib/aero/aero-cli/bin/aero" "$@"
EOF
chmod +x "${PKG_DIR}/usr/bin/aero"

# 4. GUI wrappers in /usr/bin
for script in $(find "${ROOT_DIR}/packages/aero-welcome/bin" -maxdepth 1 -type f -exec basename {} \;); do
    cat << EOF > "${PKG_DIR}/usr/bin/${script}"
#!/usr/bin/env bash
export PYTHONPATH="/usr/lib/aero/aero-cli:${PYTHONPATH:-}"
exec python3 "/usr/lib/aero/aero-welcome/bin/${script}" "\$@"
EOF
    chmod +x "${PKG_DIR}/usr/bin/${script}"
done

# 5. Icons, Man Pages & Completions
cp "${ROOT_DIR}/desktop/icons/aero-logo.svg" "${PKG_DIR}/usr/share/icons/hicolor/scalable/apps/aero.svg"
gzip -c "${ROOT_DIR}/docs/man/aero.1" > "${PKG_DIR}/usr/share/man/man1/aero.1.gz"
cp "${ROOT_DIR}/build/completions/aero.bash" "${PKG_DIR}/usr/share/bash-completion/completions/aero"
cp "${ROOT_DIR}/build/completions/aero.fish" "${PKG_DIR}/usr/share/fish/vendor_completions.d/aero.fish"
cp "${ROOT_DIR}/build/completions/aero.zsh" "${PKG_DIR}/usr/share/zsh/vendor-completions/_aero"

# 6. Desktop Entries
desktop_entries=(
  "aero-welcome:Aero Control Center:System Settings and Control Hub:aero:System;Settings;GTK;"
  "aero-ai-gui:Aero Local AI Studio:Offline LLM Serving & Model Manager:system-search:Development;ArtificialIntelligence;GTK;"
  "aero-spotlight:Aero Spotlight:Raycast-style Universal Command Bar:system-search:Utility;GTK;"
  "aero-monitor:Aero System Monitor:Real-time CPU Waveform Task Manager:utilities-system-monitor:System;Monitor;GTK;"
  "aero-updater:Aero Update Manager:System Patches and Package Updates:system-software-update:System;PackageManager;GTK;"
  "aero-wifi:Aero Wi-Fi Center:Wireless Networks Scanner:network-wireless:Settings;HardwareSettings;GTK;"
  "aero-bluetooth:Aero Bluetooth Center:Bluetooth Pairing & Devices:bluetooth:Settings;HardwareSettings;GTK;"
  "aero-audio:Aero Audio Center:PipeWire Audio Output Switcher:audio-volume-high:Settings;HardwareSettings;GTK;"
  "aero-displays:Aero Displays:HiDPI Scaling & Refresh Rates:preferences-desktop-display:Settings;HardwareSettings;GTK;"
  "aero-gamehub:Aero Game Hub:GameMode Boost & Proton Launcher:applications-games:Game;GTK;"
  "aero-connect-gui:Aero Phone Link:Wireless Android and iOS File Transfer:phone:Utility;GTK;"
  "aero-power-gui:Aero Battery Studio:Battery Health & Fan Cooling Curves:battery:Settings;HardwareSettings;GTK;"
  "aero-nightlight-gui:Aero Night Light:Blue Light Filter & Color Temperature:display:Settings;DesktopSettings;GTK;"
  "aero-theme-gui:Aero Theme Studio:Cyber Palette & Dynamic Wallpapers:preferences-desktop-theme:Settings;DesktopSettings;GTK;"
  "aero-cleaner-gui:Aero System Cleaner:Storage & Cache Purger:edit-clear:System;Utility;GTK;"
  "aero-snapshots-gui:Aero TimeMachine Snapshots:System Restore Points & Backups:document-revert:System;Utility;GTK;"
  "aero-vault-gui:Aero Secrets Vault:Encrypted Passwords & Tokens Keyring:security-high:Utility;Security;GTK;"
  "aero-screenshot-gui:Aero Snipping Tool:Region Snip & Screen Capture:applets-screenshooter:Utility;GTK;"
  "aero-repair-gui:Aero System Self-Repair:1-Click System Integrity Healer:system-run:System;Utility;GTK;"
  "aero-notes-gui:Aero Scratchpad Notes:Floating Developer Markdown Scratchpad:text-editor:Utility;TextEditor;GTK;"
  "aero-color-gui:Aero Color Dropper:Screen Color Picker & Palette Studio:color-picker:Graphics;Utility;GTK;"
  "aero-font-gui:Aero Typography Studio:Coding Ligatures & Font Previewer:font:Settings;DesktopSettings;GTK;"
  "aero-ports-gui:Aero Port Inspector:Dev Server & TCP/UDP Port Scanner:network-server:Development;Network;GTK;"
  "aero-shortcuts-gui:Aero Shortcuts Guide:Interactive Keyboard Hotkeys Cheatsheet:input-keyboard:Utility;Documentation;GTK;"
  "aero-flasher-gui:Aero USB Flasher:Safe Live ISO USB Creator:drive-removable-media:System;Utility;GTK;"
  "aero-logs-gui:Aero System Logs:Live Journald & Kernel Diagnostic Viewer:utilities-terminal:System;Monitor;GTK;"
  "aero-services-gui:Aero Service Manager:Systemd Daemons & Background Services:system-run:System;Settings;GTK;"
  "aero-startup-gui:Aero Startup Applications:Login Autostart Programs:system-run:Settings;DesktopSettings;GTK;"
  "aero-sync-gui:Aero Dotfiles Sync:Configs & Settings Cloud Sync:folder-cloud:Utility;Settings;GTK;"
  "aero-disk-gui:Aero Disk Visualizer:Storage & Developer Bloat Cleaner:drive-harddisk:System;Utility;GTK;"
  "aero-speed-gui:Aero Network Speed & Latency:Latency Profiler & DNS Speed Tester:network-wireless:System;Network;GTK;"
  "aero-git-gui:Aero Git Dashboard:Local Git Repositories Monitor:git:Development;GTK;"
  "aero-firewall-gui:Aero Firewall & Shield:UFW Firewall & Port Rules Studio:security-high:System;Security;GTK;"
  "aero-ssh-gui:Aero SSH & Remote Servers:SSH Keys Generator & Server Bookmarks:utilities-terminal:Network;Development;GTK;"
  "aero-ssl-gui:Aero SSL & Dev Certs:Local HTTPS SSL/TLS Certificates Studio:security-medium:Development;Security;GTK;"
  "aero-workspaces-gui:Aero Workspaces & Desktops:Virtual Workspaces & Window Organizer:preferences-desktop-workspaces:Settings;DesktopSettings;GTK;"
)

for item in "${desktop_entries[@]}"; do
    IFS=":" read -r exec_bin name comment icon categories <<< "${item}"
    cat << EOF > "${PKG_DIR}/usr/share/applications/${exec_bin}.desktop"
[Desktop Entry]
Name=${name}
Comment=${comment}
Exec=${exec_bin}
Icon=${icon}
Terminal=false
Type=Application
Categories=${categories}
EOF
done

# 7. Build .deb package
dpkg-deb --build --root-owner-group "${PKG_DIR}" "${DIST_DIR}/${PKG_NAME}_${VERSION}_${ARCH}.deb"
rm -rf "${PKG_DIR}"

echo "✅ Debian package generated at: ${DIST_DIR}/${PKG_NAME}_${VERSION}_${ARCH}.deb"
ls -lh "${DIST_DIR}/${PKG_NAME}_${VERSION}_${ARCH}.deb"
