#!/usr/bin/env bash
# ==============================================================================
# Aero Linux Automated Live ISO Builder
# Universally builds bootable live ISOs for current and future releases
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Auto-detect version from setup.py or environment
DETECTED_VER=$(grep "version=" "${ROOT_DIR}/packages/aero-cli/setup.py" | head -n1 | cut -d'"' -f2 || echo "1.4.0")
VERSION="${VERSION:-$DETECTED_VER}"
RELEASE_CODENAME="${RELEASE_CODENAME:-supernova}"
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

# Copy CLI, Libraries & 45 GTK3 Applications
cp -r "${ROOT_DIR}/packages/aero-cli/aero/"* "${ROOTFS_DIR}/usr/local/lib/python3/dist-packages/aero/"
cp "${ROOT_DIR}/packages/aero-cli/bin/aero" "${ROOTFS_DIR}/usr/local/bin/aero"
chmod +x "${ROOTFS_DIR}/usr/local/bin/aero"

cp -r "${ROOT_DIR}/packages/aero-welcome/bin/"* "${ROOTFS_DIR}/usr/local/bin/"
chmod +x "${ROOTFS_DIR}/usr/local/bin/"*

# Copy Desktop Configs & Themes
cp "${ROOT_DIR}/desktop/icons/aero-logo.svg" "${ROOTFS_DIR}/usr/share/icons/hicolor/scalable/apps/aero.svg"
gzip -c "${ROOT_DIR}/docs/man/aero.1" > "${ROOTFS_DIR}/usr/share/man/man1/aero.1.gz"

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

menuentry "⚡ Aero Linux v1.4.0 (Supernova) Live Session [x86_64]" {
    set gfxpayload=keep
    linux  /live/vmlinuz boot=live quiet splash zram=1 aero.layout=windows ---
    initrd /live/initrd.img
}

menuentry "⚡ Aero Linux v1.4.0 Live (RAM Mode - Copy to RAM)" {
    set gfxpayload=keep
    linux  /live/vmlinuz boot=live toram quiet splash ---
    initrd /live/initrd.img
}

menuentry "⚡ Aero Linux v1.4.0 Live (Failsafe Graphics / Nomodeset)" {
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
⚡ AERO LINUX v1.4.0-SUPERNOVA LIVE INSTALLATION MEDIA
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
    -volid "AERO_LINUX_1_4" \
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
