"""Configuration management"""

import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # Opinion Edge Credentials
    opinion_edge_email: str = Field(..., env='OPINION_EDGE_EMAIL')
    opinion_edge_password: str = Field(..., env='OPINION_EDGE_PASSWORD')
    
    # Base URL for Opinion Edge (configurable for panel subdomain)
    opinion_edge_base_url: str = Field(default='https://panel.opinion-edge.com', env='OPINION_EDGE_BASE_URL')

    # Proxy Configuration (all optional - leave blank to run without proxy)
    proxy_host: str = Field(default='', env='PROXY_HOST')
    proxy_port: int = Field(default=0, env='PROXY_PORT')
    proxy_username: str = Field(default='', env='PROXY_USERNAME')
    proxy_password: str = Field(default='', env='PROXY_PASSWORD')
    
    # Ollama Configuration
    ollama_host: str = Field(default='http://localhost:11434', env='OLLAMA_HOST')
    ollama_model: str = Field(default='llama3.2-vision:latest', env='OLLAMA_MODEL')
    
    # 2Captcha API (Optional - only if using paid service)
    captcha_api_key: str = Field(default='', env='CAPTCHA_API_KEY')
    
    # Persona Profile
    persona_name: str = Field(default='Dirk Baer', env='PERSONA_NAME')
    persona_address: str = Field(default='Gruenauer Strasse 48, 21635 Jork', env='PERSONA_ADDRESS')
    persona_mother_maiden: str = Field(default='Beyer', env='PERSONA_MOTHER_MAIDEN')
    persona_phone: str = Field(default='04162 70 35 67', env='PERSONA_PHONE')
    persona_country_code: str = Field(default='49', env='PERSONA_COUNTRY_CODE')
    persona_birthday: str = Field(default='10.09.1963', env='PERSONA_BIRTHDAY')
    persona_age: int = Field(default=78, env='PERSONA_AGE')
    persona_zodiac: str = Field(default='Virgo', env='PERSONA_ZODIAC')
    persona_geo_lat: float = Field(default=53.578107, env='PERSONA_GEO_LAT')
    persona_geo_lon: float = Field(default=9.698209, env='PERSONA_GEO_LON')
    
    # Automation Settings
    max_retries: int = Field(default=3, env='MAX_RETRIES')
    action_delay_min: int = Field(default=3, env='ACTION_DELAY_MIN')
    action_delay_max: int = Field(default=8, env='ACTION_DELAY_MAX')
    screenshot_cleanup_interval: int = Field(default=1200, env='SCREENSHOT_CLEANUP_INTERVAL')
    log_rotation_size_mb: int = Field(default=10, env='LOG_ROTATION_SIZE_MB')
    log_retention_count: int = Field(default=5, env='LOG_RETENTION_COUNT')
    
    # Backup Settings
    backup_enabled: bool = Field(default=True, env='BACKUP_ENABLED')
    backup_interval_hours: int = Field(default=1, env='BACKUP_INTERVAL_HOURS')
    backup_retention_days: int = Field(default=30, env='BACKUP_RETENTION_DAYS')
    backup_type: str = Field(default='local', env='BACKUP_TYPE')
    
    # Monitoring
    flask_port: int = Field(default=5000, env='FLASK_PORT')
    flask_debug: bool = Field(default=False, env='FLASK_DEBUG')
    flask_secret_key: str = Field(default='', env='FLASK_SECRET_KEY')
    
    # Dashboard authentication (optional)
    dashboard_username: str = Field(default='', env='DASHBOARD_USERNAME')
    dashboard_password: str = Field(default='', env='DASHBOARD_PASSWORD')
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    logs_dir: Path = base_dir / 'logs'
    screenshots_dir: Path = base_dir / 'screenshots'
    data_dir: Path = base_dir / 'data'
    cookies_dir: Path = data_dir / 'cookies'
    backups_dir: Path = data_dir / 'backups'
    surveys_dir: Path = data_dir / 'surveys'
    
    @property
    def proxy_enabled(self) -> bool:
        """Check if proxy is configured"""
        return bool(self.proxy_host and self.proxy_port)

    @property
    def proxy_url(self) -> str:
        """Get formatted proxy URL"""
        if not self.proxy_enabled:
            return ''
        if self.proxy_username and self.proxy_password:
            return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
        return f"http://{self.proxy_host}:{self.proxy_port}"

    @property
    def effective_secret_key(self) -> str:
        """Return configured secret key or generate a stable one from credentials"""
        if self.flask_secret_key:
            return self.flask_secret_key
        # Derive a stable key from credentials so it survives restarts
        seed = f"{self.opinion_edge_email}:{self.opinion_edge_password}:survey-automation"
        return hashlib.sha256(seed.encode()).hexdigest()
    
    @property
    def persona_dict(self) -> dict:
        """Get persona as dictionary"""
        return {
            'name': self.persona_name,
            'address': self.persona_address,
            'mother_maiden': self.persona_mother_maiden,
            'phone': self.persona_phone,
            'country_code': self.persona_country_code,
            'birthday': self.persona_birthday,
            'age': self.persona_age,
            'zodiac': self.persona_zodiac,
            'geo_lat': self.persona_geo_lat,
            'geo_lon': self.persona_geo_lon
        }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories
        for dir_path in [self.logs_dir, self.screenshots_dir, self.data_dir,
                         self.cookies_dir, self.backups_dir, self.surveys_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
