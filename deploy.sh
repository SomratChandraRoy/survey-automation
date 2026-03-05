#!/bin/bash

set -e

echo "================================================"
echo "Opinion Edge Survey Automation - Deployment"
echo "================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please do not run as root${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if .env exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

print_status "Environment file found"

# Update system
print_status "Updating system packages..."
sudo apt-get update -qq

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    unzip \
    chromium-browser \
    chromium-chromedriver \
    xvfb \
    supervisor \
    > /dev/null 2>&1

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    print_status "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    print_status "Ollama already installed"
fi

# Start Ollama service
print_status "Starting Ollama service..."
sudo systemctl enable ollama || true
sudo systemctl start ollama || true

# Pull Ollama vision model
print_status "Pulling Ollama vision model (this may take a while)..."
ollama pull llama3.2-vision:latest

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p logs screenshots data/cookies data/backups data/surveys

# Set permissions
chmod +x main.py

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/survey-automation.service > /dev/null <<EOF
[Unit]
Description=Opinion Edge Survey Automation
After=network.target ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/main.py
Restart=always
RestartSec=10
StartLimitInterval=200
StartLimitBurst=5
StandardOutput=append:$(pwd)/logs/automation.log
StandardError=append:$(pwd)/logs/error.log

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$(pwd)/logs $(pwd)/screenshots $(pwd)/data $(pwd)/.env

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
print_status "Enabling and starting automation service..."
sudo systemctl enable survey-automation
sudo systemctl start survey-automation

# Wait a moment for service to start
sleep 3

# Check service status
if sudo systemctl is-active --quiet survey-automation; then
    print_status "Service started successfully!"
else
    print_error "Service failed to start. Check logs:"
    echo "  sudo journalctl -u survey-automation -n 50"
    exit 1
fi

echo ""
echo "================================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "================================================"
echo ""
echo "📊 Monitoring Dashboard: http://$(hostname -I | awk '{print $1}'):5000"
echo "📝 View Logs: tail -f logs/automation.log"
echo "🔍 Service Status: sudo systemctl status survey-automation"
echo "🔄 Restart Service: sudo systemctl restart survey-automation"
echo "🛑 Stop Service: sudo systemctl stop survey-automation"
echo ""
echo "The automation is now running in the background!"
echo ""
