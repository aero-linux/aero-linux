#!/bin/bash
# Scans active listening TCP ports for developers (e.g. 3000, 8000, 8080, 5432)

ports=$(ss -tulpn 2>/dev/null | grep -E "LISTEN" | awk '{print $5}' | awk -F: '{print $NF}' | grep -E "^[0-9]+$" | sort -nu | head -n 4 | tr '\n' ' ' | sed 's/ $//')

if [ -n "$ports" ]; then
    port_list=$(echo "$ports" | sed 's/ / :/g')
    echo "{\"text\": \"🔌 :${port_list}\", \"class\": \"active\", \"tooltip\": \"Active Dev Ports Listening:\\n${ports}\\nClick to open Port Inspector\"}"
else
    echo "{\"text\": \"🔌 No Ports\", \"class\": \"idle\", \"tooltip\": \"No active dev server ports listening\\nClick to open Port Inspector\"}"
fi
