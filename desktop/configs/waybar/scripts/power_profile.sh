#!/bin/bash
# Returns active CPU scaling profile for Waybar

gov=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "powersave")

case "$gov" in
    "powersave")
        echo "{\"text\": \"🔋 Battery\", \"class\": \"powersave\", \"tooltip\": \"Quiet fan & max battery preservation\"}"
        ;;
    "performance")
        echo "{\"text\": \"🚀 Boost\", \"class\": \"performance\", \"tooltip\": \"Full multi-core boost active\"}"
        ;;
    *)
        echo "{\"text\": \"⚡ Balanced\", \"class\": \"balanced\", \"tooltip\": \"Dynamic CPU scaling active\"}"
        ;;
esac
