#!/bin/bash

# Stop automation script

echo "Stopping Survey Automation..."

# Stop systemd service if exists
if systemctl is-active --quiet survey-automation; then
    sudo systemctl stop survey-automation
    echo "✓ Systemd service stopped"
fi

# Kill any running Python processes
pkill -f "main.py"
echo "✓ Python processes terminated"

echo "Automation stopped successfully"
