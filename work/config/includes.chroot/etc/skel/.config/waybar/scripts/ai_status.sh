#!/bin/bash
# Returns Ollama local AI status for Waybar

if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    models_count=$(curl -s http://127.0.0.1:11434/api/tags | grep -o '"name":' | wc -l)
    echo "{\"text\": \"🤖 AI (${models_count})\", \"class\": \"ready\", \"tooltip\": \"Ollama AI daemon ready. Models: ${models_count}\"}"
else
    echo "{\"text\": \"🤖 AI Idle\", \"class\": \"idle\", \"tooltip\": \"Local AI daemon offline (Run 'aero ai init')\"}"
fi
