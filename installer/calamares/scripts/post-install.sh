#!/bin/bash
# Aero Linux Post-Install Automation Script (Invoked by Calamares)

set -e

echo "⚡ Applying Aero Linux post-install optimizations..."

# 1. Enable zRAM service
if command -v systemctl >/dev/null 2>&1; then
    systemctl enable systemd-zram-setup@zram0.service 2>/dev/null || true
    systemctl enable tlp.service 2>/dev/null || true
    systemctl enable docker.service 2>/dev/null || true
fi

# 2. Setup user groups for Docker and Video hardware acceleration
for user in $(awk -F: '$3 >= 1000 && $1 != "nobody" {print $1}' /etc/passwd); do
    usermod -aG docker,video,render,audio "$user" 2>/dev/null || true
done

# 3. Apply low-latency sysctl settings
sysctl --system 2>/dev/null || true

# 4. Set Aero fish aliases as default
if [ -d /etc/skel/.config/fish ]; then
    mkdir -p /etc/fish
    cp /etc/skel/.config/fish/config.fish /etc/fish/config.fish 2>/dev/null || true
fi

echo "✅ Aero Linux post-installation configuration complete!"
