#!/bin/bash

#############################################
# One-Command Installation Script
# Automated setup for Ubuntu/Linux servers
#############################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/installation.log"
REQUIRED_PYTHON_VERSION="3.8"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

check_root() {
    if [ "$EUID" -eq 0 ]; then 
        error "Please do not run as root. Run as regular user with sudo privileges."
    fi
}

check_os() {
    if [ ! -f /etc/os-release ]; then
        error "Cannot detect OS. This script requires Ubuntu/Debian Linux."
    fi
    
    . /etc/os-release
    if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
        warn "This script is optimized for Ubuntu/Debian. Your OS: $ID"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log "OS detected: $PRETTY_NAME"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed. Installing..."
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$PYTHON_VERSION < $REQUIRED_PYTHON_VERSION" | bc -l) )); then
        error "Python $REQUIRED_PYTHON_VERSION+ required. Found: $PYTHON_VERSION"
    fi
    
    log "Python version: $PYTHON_VERSION ✓"
}

install_system_dependencies() {
    log "Installing system dependencies..."
    
    sudo apt-get update -qq || error "Failed to update package lists"
    
    PACKAGES=(
        "python3"
        "python3-pip"
        "python3-venv"
        "python3-dev"
        "build-essential"
        "wget"
        "curl"
        "git"
        "unzip"
        "chromium-browser"
        "chromium-chromedriver"
        "portaudio19-dev"
        "python3-pyaudio"
        "ffmpeg"
        "libsndfile1"
        "supervisor"
        "nginx"
        "certbot"
        "python3-certbot-nginx"
    )
    
    for package in "${PACKAGES[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package"; then
            info "Installing $package..."
            sudo apt-get install -y "$package" >> "$LOG_FILE" 2>&1 || warn "Failed to install $package"
        fi
    done
    
    log "System dependencies installed ✓"
}

install_ollama() {
    if command -v ollama &> /dev/null; then
        log "Ollama already installed ✓"
        return
    fi
    
    log "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh >> "$LOG_FILE" 2>&1 || error "Failed to install Ollama"
    
    # Start and enable Ollama service
    sudo systemctl enable ollama >> "$LOG_FILE" 2>&1
    sudo systemctl start ollama >> "$LOG_FILE" 2>&1
    
    # Wait for Ollama to start
    sleep 5
    
    log "Ollama installed ✓"
}

pull_ollama_model() {
    log "Pulling Ollama vision model (this may take 5-10 minutes)..."
    
    ollama pull llama3.2-vision:latest >> "$LOG_FILE" 2>&1 || error "Failed to pull Ollama model"
    
    log "Ollama model downloaded ✓"
}

setup_python_environment() {
    log "Setting up Python virtual environment..."
    
    cd "$SCRIPT_DIR"
    
    # Create venv
    python3 -m venv venv || error "Failed to create virtual environment"
    
    # Activate venv
    source venv/bin/activate || error "Failed to activate virtual environment"
    
    # Upgrade pip
    pip install --upgrade pip >> "$LOG_FILE" 2>&1 || error "Failed to upgrade pip"
    
    # Install requirements
    log "Installing Python dependencies..."
    pip install -r requirements.txt >> "$LOG_FILE" 2>&1 || error "Failed to install Python dependencies"
    
    log "Python environment setup ✓"
}

create_directories() {
    log "Creating directory structure..."
    
    mkdir -p logs screenshots data/cookies data/backups data/surveys
    chmod 755 logs screenshots data
    
    log "Directories created ✓"
}

configure_environment() {
    if [ -f .env ]; then
        log ".env file already exists ✓"
        return
    fi
    
    log "Creating .env configuration file..."
    cp .env.example .env || error "Failed to create .env file"
    
    echo ""
    echo "=========================================="
    echo "CONFIGURATION REQUIRED"
    echo "=========================================="
    echo ""
    echo "Please configure your .env file with:"
    echo "1. Opinion Edge credentials"
    echo "2. Proxy settings (optional)"
    echo "3. Persona information"
    echo ""
    read -p "Open .env file now for editing? (Y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        ${EDITOR:-nano} .env
    fi
    
    log ".env file created ✓"
}

validate_configuration() {
    log "Validating configuration..."
    
    if [ ! -f .env ]; then
        error ".env file not found"
    fi
    
    # Check required variables
    source .env
    
    REQUIRED_VARS=(
        "OPINION_EDGE_EMAIL"
        "OPINION_EDGE_PASSWORD"
        "OLLAMA_HOST"
        "OLLAMA_MODEL"
    )
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            error "Required variable $var is not set in .env"
        fi
    done
    
    log "Configuration validated ✓"
}

create_systemd_service() {
    log "Creating systemd service..."
    
    SERVICE_FILE="/etc/systemd/system/survey-automation.service"
    
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Opinion Edge Survey Automation
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
Environment="PATH=$SCRIPT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$SCRIPT_DIR/venv/bin/python3 $SCRIPT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$SCRIPT_DIR/logs/automation.log
StandardError=append:$SCRIPT_DIR/logs/error.log

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$SCRIPT_DIR/logs $SCRIPT_DIR/screenshots $SCRIPT_DIR/data

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable survey-automation
    
    log "Systemd service created ✓"
}

configure_nginx() {
    log "Configuring Nginx reverse proxy..."
    
    NGINX_CONF="/etc/nginx/sites-available/survey-automation"
    
    sudo tee "$NGINX_CONF" > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF
    
    sudo ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    sudo nginx -t && sudo systemctl reload nginx
    
    log "Nginx configured ✓"
}

run_health_check() {
    log "Running health check..."
    
    source venv/bin/activate
    python3 -c "
import sys
sys.path.insert(0, '.')
from src.config.settings import Settings
from src.utils.error_tracker import HealthChecker

try:
    settings = Settings()
    checker = HealthChecker(settings)
    results = checker.check_all()
    
    if results['overall_status'] == 'healthy':
        print('✓ Health check passed')
        sys.exit(0)
    else:
        print('⚠ Health check warnings:')
        for check, result in results['checks'].items():
            if result['status'] != 'ok':
                print(f'  - {check}: {result[\"message\"]}')
        sys.exit(1)
except Exception as e:
    print(f'✗ Health check failed: {e}')
    sys.exit(1)
" || warn "Health check completed with warnings"
    
    log "Health check completed ✓"
}

start_service() {
    log "Starting survey automation service..."
    
    sudo systemctl start survey-automation
    sleep 3
    
    if sudo systemctl is-active --quiet survey-automation; then
        log "Service started successfully ✓"
    else
        error "Service failed to start. Check logs: sudo journalctl -u survey-automation -n 50"
    fi
}

print_summary() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}INSTALLATION COMPLETE!${NC}"
    echo "=========================================="
    echo ""
    echo "📊 Dashboard: http://$(hostname -I | awk '{print $1}'):5000"
    echo "📝 Logs: tail -f $SCRIPT_DIR/logs/automation.log"
    echo "🔍 Status: sudo systemctl status survey-automation"
    echo "🔄 Restart: sudo systemctl restart survey-automation"
    echo "🛑 Stop: sudo systemctl stop survey-automation"
    echo ""
    echo "Next steps:"
    echo "1. Verify .env configuration"
    echo "2. Check dashboard is accessible"
    echo "3. Monitor logs for first survey"
    echo ""
    echo "💰 Start earning money now!"
    echo ""
}

# Main installation flow
main() {
    echo "=========================================="
    echo "Survey Automation - One-Command Install"
    echo "=========================================="
    echo ""
    
    log "Starting installation..."
    
    check_root
    check_os
    check_python
    install_system_dependencies
    install_ollama
    pull_ollama_model
    setup_python_environment
    create_directories
    configure_environment
    validate_configuration
    create_systemd_service
    configure_nginx
    run_health_check
    start_service
    print_summary
    
    log "Installation completed successfully!"
}

# Run main function
main "$@"
