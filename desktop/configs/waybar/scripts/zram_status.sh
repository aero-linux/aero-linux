#!/bin/bash
# Returns zRAM compression metrics for Waybar custom module with rich tooltip

if [ -f /proc/swaps ] && grep -q "zram" /proc/swaps; then
    orig_bytes=$(cat /sys/block/zram0/orig_data_size 2>/dev/null || echo 0)
    comp_bytes=$(cat /sys/block/zram0/compr_data_size 2>/dev/null || echo 0)
    mem_used_bytes=$(cat /sys/block/zram0/mem_used_total 2>/dev/null || echo 0)
    
    if [ "$orig_bytes" -gt 0 ] && [ "$comp_bytes" -gt 0 ]; then
        ratio=$(awk "BEGIN {printf \"%.1f\", $orig_bytes/$comp_bytes}")
        orig_mb=$((orig_bytes / 1024 / 1024))
        comp_mb=$((comp_bytes / 1024 / 1024))
        saved_mb=$((orig_mb - comp_mb))
        echo "{\"text\": \"🧠 zRAM ${ratio}x (${orig_mb}MB)\", \"class\": \"active\", \"tooltip\": \"zRAM ZSTD Active\\n• Uncompressed: ${orig_mb} MB\\n• In-RAM Size: ${comp_mb} MB\\n• RAM Space Saved: ${saved_mb} MB\\nClick to open Cleaner & Optimizer\"}"
    else
        echo "{\"text\": \"🧠 zRAM Active\", \"class\": \"active\", \"tooltip\": \"zRAM ZSTD Active (0MB compressed data)\\nClick to open Cleaner & Optimizer\"}"
    fi
else
    echo "{\"text\": \"🧠 zRAM Off\", \"class\": \"disabled\", \"tooltip\": \"zRAM not active\\nRun 'sudo systemctl restart aero-zram'\"}"
fi
