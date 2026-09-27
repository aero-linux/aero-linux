#!/bin/bash
# Returns zRAM compression metrics for Waybar custom module

if [ -f /proc/swaps ] && grep -q "zram" /proc/swaps; then
    orig_kb=$(cat /sys/block/zram0/orig_data_size 2>/dev/null || echo 0)
    comp_kb=$(cat /sys/block/zram0/compr_data_size 2>/dev/null || echo 0)
    
    if [ "$orig_kb" -gt 0 ] && [ "$comp_kb" -gt 0 ]; then
        ratio=$(awk "BEGIN {printf \"%.1f\", $orig_kb/$comp_kb}")
        orig_mb=$((orig_kb / 1024 / 1024))
        echo "{\"text\": \"🧠 zRAM ${ratio}x (${orig_mb}MB)\", \"class\": \"active\", \"tooltip\": \"zRAM ZSTD Active - In-memory compressed data\"}"
    else
        echo "{\"text\": \"🧠 zRAM Active\", \"class\": \"active\", \"tooltip\": \"zRAM ZSTD Device Active\"}"
    fi
else
    echo "{\"text\": \"🧠 zRAM Off\", \"class\": \"disabled\", \"tooltip\": \"zRAM not detected\"}"
fi
