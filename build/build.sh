#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Aero Linux Automated Live ISO Generator
# ==============================================================================

DIST_NAME="Aero-Linux"
DIST_VERSION="1.2-Titan"
ARCH="amd64"
OUTPUT_DIR="output"
WORK_DIR="work"
ISO_NAME="${DIST_NAME}-${DIST_VERSION}-${ARCH}.iso"

echo "=========================================================="
echo "⚡ Building ${DIST_NAME} ${DIST_VERSION} (${ARCH})"
echo "=========================================================="

# Check root permissions
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run build.sh as root (sudo ./build.sh)"
    exit 1
fi

mkdir -p "${OUTPUT_DIR}" "${WORK_DIR}"

echo "📦 Initializing Live Build configuration..."
# Export environment
export LIVE_BUILD_RELEASE="noble"

# Copy package configurations & sysctl
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/sysctl.d"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/default"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/tlp.d"
mkdir -p "${WORK_DIR}/config/includes.chroot/usr/local/bin"

cp build/config/kernel.conf "${WORK_DIR}/config/includes.chroot/etc/sysctl.d/99-aero-performance.conf"
cp build/config/zram.conf "${WORK_DIR}/config/includes.chroot/etc/default/zramswap"
cp build/config/tlp-custom.conf "${WORK_DIR}/config/includes.chroot/etc/tlp.d/99-aero-power.conf"

# Copy Aero CLI & Python backend packages into chroot
mkdir -p "${WORK_DIR}/config/includes.chroot/usr/local/lib/python3/dist-packages"
cp -r packages/aero-cli/aero "${WORK_DIR}/config/includes.chroot/usr/local/lib/python3/dist-packages/"
cp packages/aero-cli/bin/aero "${WORK_DIR}/config/includes.chroot/usr/local/bin/aero"
chmod +x "${WORK_DIR}/config/includes.chroot/usr/local/bin/aero"

# Copy all Aero Graphical Applications
cp -r packages/aero-welcome/bin/* "${WORK_DIR}/config/includes.chroot/usr/local/bin/"
chmod +x "${WORK_DIR}/config/includes.chroot/usr/local/bin/"*

# Copy Nemo File Manager Actions
mkdir -p "${WORK_DIR}/config/includes.chroot/usr/share/nemo/actions"
cp -r desktop/configs/nemo-actions/*.nemo_action "${WORK_DIR}/config/includes.chroot/usr/share/nemo/actions/" 2>/dev/null || true

# Stage Desktop Dotfiles into /etc/skel (Default user configuration)
echo "🎨 Staging Aero Cyber Dark desktop dotfiles into /etc/skel..."
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/sway"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/alacritty"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/fish"

cp desktop/configs/sway/config "${WORK_DIR}/config/includes.chroot/etc/skel/.config/sway/config"
cp desktop/configs/waybar/config "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar/config"
cp desktop/configs/waybar/style.css "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar/style.css"
cp desktop/configs/alacritty/alacritty.toml "${WORK_DIR}/config/includes.chroot/etc/skel/.config/alacritty/alacritty.toml"
cp desktop/configs/fish/config.fish "${WORK_DIR}/config/includes.chroot/etc/skel/.config/fish/config.fish"

# Stage Swaylock and Swayidle
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/swaylock"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/swayidle"
cp desktop/configs/swaylock/config "${WORK_DIR}/config/includes.chroot/etc/skel/.config/swaylock/config"
cp desktop/configs/swayidle/config "${WORK_DIR}/config/includes.chroot/etc/skel/.config/swayidle/config"

# Stage Waybar scripts
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar/scripts"
cp desktop/configs/waybar/scripts/*.sh "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar/scripts/"
chmod +x "${WORK_DIR}/config/includes.chroot/etc/skel/.config/waybar/scripts/"*.sh

# Stage Shell Completions
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/fish/completions"
mkdir -p "${WORK_DIR}/config/includes.chroot/etc/bash_completion.d"
cp build/completions/aero.fish "${WORK_DIR}/config/includes.chroot/etc/fish/completions/aero.fish"
cp build/completions/aero.bash "${WORK_DIR}/config/includes.chroot/etc/bash_completion.d/aero"

# Stage Plymouth Boot Theme
mkdir -p "${WORK_DIR}/config/includes.chroot/usr/share/plymouth/themes/aero"
cp desktop/themes/plymouth/aero/* "${WORK_DIR}/config/includes.chroot/usr/share/plymouth/themes/aero/"

# Stage Calamares Post-Install Hook
mkdir -p "${WORK_DIR}/config/includes.chroot/usr/share/calamares/scripts"
cp installer/calamares/scripts/post-install.sh "${WORK_DIR}/config/includes.chroot/usr/share/calamares/scripts/post-install.sh"
chmod +x "${WORK_DIR}/config/includes.chroot/usr/share/calamares/scripts/post-install.sh"

echo "✅ Build staging complete. Ready to assemble ISO: ${OUTPUT_DIR}/${ISO_NAME}"
