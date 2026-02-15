#!/bin/bash

# Quick local run script (for testing)

echo "Starting Survey Automation (Local Mode)"
echo "========================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if venv exists
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create directories
mkdir -p logs screenshots data/cookies data/backups data/surveys

# Run automation
echo "Starting automation..."
python3 main.py
