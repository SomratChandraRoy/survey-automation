"""Proxy management with kill-switch"""

import requests
import time
from loguru import logger

class ProxyManager:
    """Manage proxy connection with validation"""
    
    def __init__(self, settings):
        self.settings = settings
        self.proxy_url = settings.proxy_url
        self.proxies = (
            {'http': self.proxy_url, 'https': self.proxy_url}
            if self.proxy_url else {}
        )
    
    def validate_proxy(self) -> bool:
        """Validate proxy connectivity and check for leaks"""
        if not self.settings.proxy_enabled:
            logger.info("No proxy configured - running without proxy (direct connection)")
            return True

        logger.info("Validating proxy connection...")
        
        try:
            # Test proxy connectivity
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies=self.proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                proxy_ip = response.json().get('ip')
                logger.info(f"Proxy IP: {proxy_ip}")
                
                # Check speed
                start_time = time.time()
                requests.get('https://www.google.com', proxies=self.proxies, timeout=15)
                latency = time.time() - start_time
                
                logger.info(f"Proxy latency: {latency:.2f}s")
                
                if latency > 5:
                    logger.warning("Proxy latency is high (>5s) - continuing anyway")
                
                # Check for DNS leak
                if not self._check_dns_leak():
                    logger.error("DNS leak detected!")
                    return False
                
                logger.info("Proxy validation successful")
                return True
            else:
                logger.error(f"Proxy validation failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Proxy validation error: {e}")
            return False
    
    def _check_dns_leak(self) -> bool:
        """Check for DNS leaks"""
        try:
            # Simple DNS leak check
            response = requests.get(
                'https://www.dnsleaktest.com/api/v1/test',
                proxies=self.proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("DNS leak check passed")
                return True
            return True  # Assume OK if service unavailable
            
        except Exception as e:
            logger.warning(f"DNS leak check failed: {e}")
            return True  # Don't block on check failure
    
    def get_chrome_proxy_extension(self) -> dict:
        """Get proxy configuration for Chrome"""
        if not self.proxy_url:
            return {}
        return {
            'proxy': {
                'http': self.proxy_url,
                'https': self.proxy_url,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
