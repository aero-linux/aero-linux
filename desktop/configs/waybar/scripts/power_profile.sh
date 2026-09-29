#!/bin/bash
# Returns active CPU scaling profile for Waybar with rich interactive tooltips

gov=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "powersave")

case "$gov" in
    "powersave")
        echo "{\"text\": \"🔋 Quiet\", \"class\": \"powersave\", \"tooltip\": \"Power Profile: Quiet & Battery Preservation\\n• Fan curves minimized\\n• ACPI 80% charge threshold respected\\nClick to open Battery Studio\"}"
        ;;
    "performance")
        echo "{\"text\": \"🚀 Boost\", \"class\": \"performance\", \"tooltip\": \"Power Profile: Turbo Boost (Full Multi-Core)\\n• Maximum clocks & thermals\\nClick to open Battery Studio\"}"
        ;;
    *)
        echo "{\"text\": \"⚡ Balanced\", \"class\": \"balanced\", \"tooltip\": \"Power Profile: Balanced Dynamic Scaling\\n• Dynamic frequency governor active\\nClick to open Battery Studio\"}"
        ;;
esac
