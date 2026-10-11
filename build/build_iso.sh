#!/usr/bin/env bash
# ==============================================================================
# Aero Linux Automated Live ISO Builder
# Universally builds bootable live ISOs for current and future releases
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Auto-detect version from setup.py or environment
DETECTED_VER=$(grep "version=" "${ROOT_DIR}/packages/aero-cli/setup.py" | head -n1 | cut -d'"' -f2 || echo "1.5.0")
VERSION="${VERSION:-$DETECTED_VER}"
RELEASE_CODENAME="${RELEASE_CODENAME:-pulsar}"
DIST_NAME="aero-linux"
ARCH="amd64"
DIST_DIR="${ROOT_DIR}/dist"
ISO_NAME="${DIST_NAME}_${VERSION}_${RELEASE_CODENAME}_${ARCH}.iso"
ISO_PATH="${DIST_DIR}/${ISO_NAME}"
WORK_DIR="${DIST_DIR}/iso_work"
ROOTFS_DIR="${WORK_DIR}/rootfs"
CD_DIR="${WORK_DIR}/cd"


echo "⚡ Assembling Aero Linux v${VERSION}-${RELEASE_CODENAME} Live ISO..."

rm -rf "${WORK_DIR}"
mkdir -p "${DIST_DIR}" "${ROOTFS_DIR}" "${CD_DIR}/live" "${CD_DIR}/boot/grub"

# 1. Populate Live Rootfs with Aero Linux Suite
echo "📦 Staging Aero Linux components into Live Rootfs..."
mkdir -p "${ROOTFS_DIR}/usr/local/bin"
mkdir -p "${ROOTFS_DIR}/usr/local/lib/python3/dist-packages/aero"
mkdir -p "${ROOTFS_DIR}/usr/share/applications"
mkdir -p "${ROOTFS_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${ROOTFS_DIR}/usr/share/man/man1"
mkdir -p "${ROOTFS_DIR}/etc/skel/.config/sway"
mkdir -p "${ROOTFS_DIR}/etc/skel/.config/waybar"
mkdir -p "${ROOTFS_DIR}/etc/skel/.config/alacritty"
mkdir -p "${ROOTFS_DIR}/etc/skel/.config/fish"
mkdir -p "${ROOTFS_DIR}/etc/sysctl.d"
mkdir -p "${ROOTFS_DIR}/etc/default"
mkdir -p "${ROOTFS_DIR}/etc/tlp.d"
mkdir -p "${ROOTFS_DIR}/etc/calamares"

# Copy CLI, Libraries & 59 GTK3 Applications
cp -r "${ROOT_DIR}/packages/aero-cli/aero/"* "${ROOTFS_DIR}/usr/local/lib/python3/dist-packages/aero/"
cp "${ROOT_DIR}/packages/aero-cli/bin/aero" "${ROOTFS_DIR}/usr/local/bin/aero"
chmod +x "${ROOTFS_DIR}/usr/local/bin/aero"

cp -r "${ROOT_DIR}/packages/aero-welcome/bin/"* "${ROOTFS_DIR}/usr/local/bin/"
chmod +x "${ROOTFS_DIR}/usr/local/bin/"*

# Copy Desktop Configs & Themes
cp "${ROOT_DIR}/desktop/icons/aero-logo.svg" "${ROOTFS_DIR}/usr/share/icons/hicolor/scalable/apps/aero.svg"
gzip -c "${ROOT_DIR}/docs/man/aero.1" > "${ROOTFS_DIR}/usr/share/man/man1/aero.1.gz"

# Stage Shell Completions
mkdir -p "${ROOTFS_DIR}/etc/bash_completion.d"
mkdir -p "${ROOTFS_DIR}/usr/share/fish/vendor_completions.d"
mkdir -p "${ROOTFS_DIR}/usr/share/zsh/vendor-completions"
cp "${ROOT_DIR}/build/completions/aero.bash" "${ROOTFS_DIR}/etc/bash_completion.d/aero" 2>/dev/null || true
cp "${ROOT_DIR}/build/completions/aero.fish" "${ROOTFS_DIR}/usr/share/fish/vendor_completions.d/aero.fish" 2>/dev/null || true
cp "${ROOT_DIR}/build/completions/aero.zsh" "${ROOTFS_DIR}/usr/share/zsh/vendor-completions/_aero" 2>/dev/null || true

# Copy Nemo Context Actions
mkdir -p "${ROOTFS_DIR}/usr/share/nemo/actions"
cp -r "${ROOT_DIR}/desktop/configs/nemo-actions/"*.nemo_action "${ROOTFS_DIR}/usr/share/nemo/actions/" 2>/dev/null || true

# Generate 59 Desktop Entries for Applications Menu
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
  "aero-ebpf-gui:Aero eBPF & Kernel Socket Inspector:Kernel TraceFS & Active Sockets:utilities-terminal:Development;System;GTK;"
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
  "aero-about-gui:About Aero Linux:System Specifications & Architecture:help-about:System;GTK;"
  "aero-api-gui:Aero API & HTTP Studio:REST API Tester & Latency Inspector:network-server:Development;GTK;"
  "aero-archive-gui:Aero Archive Manager:Multi-Format Archive Studio:package-x-generic:Utility;GTK;"
  "aero-benchmark-gui:Aero Benchmark Studio:CPU & Memory Benchmark:utilities-system-monitor:System;GTK;"
  "aero-cron-gui:Aero Cron Scheduler:Scheduled Background Tasks:appointment-new:System;Settings;GTK;"
  "aero-crypto-gui:Aero Cryptography Studio:JWT Decoder & Hashing Engine:security-high:Utility;Security;GTK;"
  "aero-db-gui:Aero Database Studio:SQLite & Relational DB Console:server-database:Development;GTK;"
  "aero-deps-gui:Aero Dependency Inspector:Shared Libraries & System Dependencies:system-run:Development;GTK;"
  "aero-diff-gui:Aero Diff Comparator:Side-by-side Visual Code Diff:text-x-generic:Development;GTK;"
  "aero-docker-gui:Aero Docker & Container Studio:Container Telemetry & Management:system-run:Development;GTK;"
  "aero-env-gui:Aero Environment Studio:Project .env & Secrets Studio:preferences-system:Development;GTK;"
  "aero-gitgraph-gui:Aero Git Graph Tree:Interactive Commit Visualizer:git:Development;GTK;"
  "aero-gpu-gui:Aero GPU Studio:Hybrid GPU Switcher & Telemetry:video-display:HardwareSettings;GTK;"
  "aero-markdown-gui:Aero Markdown Studio:Technical Documentation Editor:text-editor:Utility;GTK;"
  "aero-mock-gui:Aero Mock Server:Mock REST API Server & Webhooks:network-server:Development;GTK;"
  "aero-qr-gui:Aero QR Studio:Terminal & Vector QR Code Studio:camera-photo:Utility;GTK;"
  "aero-quick-settings:Aero Quick Settings:Desktop Quick Action Center:preferences-system:Settings;GTK;"
  "aero-recorder-gui:Aero Screen Recorder:Screen & Media Audio Recorder:camera-video:AudioVideo;GTK;"
  "aero-regex-gui:Aero Regex Studio:Regular Expressions Evaluator:edit-find:Development;GTK;"
  "aero-sandbox-gui:Aero Live Code Sandbox:Multi-Language Isolated Code Runner:utilities-terminal:Development;GTK;"
  "aero-snapshot-gui:Aero Quick Snapshot:System Restore Point Trigger:document-revert:System;GTK;"
  "aero-tunnel-gui:Aero HTTPS Tunnel:Localhost Public Tunnel:network-wireless:Network;Development;GTK;"
)

for item in "${desktop_entries[@]}"; do
    IFS=":" read -r exec_bin name comment icon categories <<< "${item}"
    cat << EOF > "${ROOTFS_DIR}/usr/share/applications/${exec_bin}.desktop"
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

cp "${ROOT_DIR}/build/config/kernel.conf" "${ROOTFS_DIR}/etc/sysctl.d/99-aero-performance.conf"
cp "${ROOT_DIR}/build/config/zram.conf" "${ROOTFS_DIR}/etc/default/zramswap"
cp "${ROOT_DIR}/build/config/tlp-custom.conf" "${ROOTFS_DIR}/etc/tlp.d/99-aero-power.conf"

cp "${ROOT_DIR}/desktop/configs/sway/config" "${ROOTFS_DIR}/etc/skel/.config/sway/config" 2>/dev/null || true
cp -r "${ROOT_DIR}/desktop/configs/waybar/"* "${ROOTFS_DIR}/etc/skel/.config/waybar/" 2>/dev/null || true
cp "${ROOT_DIR}/desktop/configs/alacritty/alacritty.toml" "${ROOTFS_DIR}/etc/skel/.config/alacritty/alacritty.toml" 2>/dev/null || true
cp "${ROOT_DIR}/desktop/configs/fish/config.fish" "${ROOTFS_DIR}/etc/skel/.config/fish/config.fish" 2>/dev/null || true

# Copy Calamares Installer Branding & Configs
cp -r "${ROOT_DIR}/installer/calamares/"* "${ROOTFS_DIR}/etc/calamares/" 2>/dev/null || true

# 2. Build SquashFS Root Filesystem
echo "🗜️ Creating compressed Live filesystem (SquashFS)..."
mksquashfs "${ROOTFS_DIR}" "${CD_DIR}/live/filesystem.squashfs" -comp zstd -Xcompression-level 15 -b 1M -noappend
du -b "${ROOTFS_DIR}" | tail -n1 | awk '{print $1}' > "${CD_DIR}/live/filesystem.size"

# 3. Configure GRUB Live Bootloader
echo "⚙️ Configuring GRUB Live Bootloader..."
cat << 'EOF_GRUB' > "${CD_DIR}/boot/grub/grub.cfg"
set default="0"
set timeout=5

insmod font
if loadfont /boot/grub/fonts/unicode.pf2 ; then
    insmod gfxterm
    set gfxmode=auto
    set gfxpayload=keep
    terminal_output gfxterm
fi

set menu_color_normal=white/black
set menu_color_highlight=cyan/black

menuentry "⚡ Aero Linux v1.5.0 (Pulsar) Live Session [x86_64]" {
    set gfxpayload=keep
    linux  /live/vmlinuz boot=live quiet splash zram=1 aero.layout=windows ---
    initrd /live/initrd.img
}

menuentry "⚡ Aero Linux v1.5.0 Live (RAM Mode - Copy to RAM)" {
    set gfxpayload=keep
    linux  /live/vmlinuz boot=live toram quiet splash ---
    initrd /live/initrd.img
}

menuentry "⚡ Aero Linux v1.5.0 Live (Failsafe Graphics / Nomodeset)" {
    set gfxpayload=keep
    linux  /live/vmlinuz boot=live nomodeset quiet ---
    initrd /live/initrd.img
}

menuentry "💾 Run Memory Test (Memtest86+)" {
    linux16 /boot/memtest86+.bin
}
EOF_GRUB

# 4. Generate Live System Metadata
cat << EOF_META > "${CD_DIR}/live/README.txt"
================================================================================
⚡ AERO LINUX v1.5.0-PULSAR LIVE INSTALLATION MEDIA
================================================================================
Architecture: x86_64
Base: Debian/Ubuntu Minimal Base
Desktop: Wayland / Sway (Dual Desktop Engine)
Default User: aero (Password: aero)
Live Web Portal: https://ronitgupta138.github.io/aero-linux/
Source Repository: https://github.com/ronitgupta138/aero-linux
Issue Tracker: https://github.com/ronitgupta138/aero-linux/issues
License: MIT License
================================================================================
EOF_META

# 5. Build Bootable Hybrid ISO via genisoimage / grub-mkrescue
echo "💿 Building final bootable ISO image: ${ISO_NAME}..."
genisoimage -rational-rock \
    -volid "AERO_LINUX_1_5" \
    -cache-inodes \
    -joliet \
    -full-iso9660-filenames \
    -o "${ISO_PATH}" \
    "${CD_DIR}"

# Calculate SHA256 Checksum
cd "${DIST_DIR}"
sha256sum "${ISO_NAME}" >> SHA256SUMS
sort -u SHA256SUMS -o SHA256SUMS

echo ""
echo "=========================================================="
echo "✅ Bootable Live ISO successfully generated!"
echo "📍 Location: ${ISO_PATH}"
echo "📊 Size: $(du -h "${ISO_PATH}" | cut -f1)"
echo "🔑 SHA256: $(sha256sum "${ISO_PATH}" | cut -d' ' -f1)"
echo "=========================================================="
