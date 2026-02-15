"""Anti-Captcha adapter (alternative to 2Captcha)"""

import time
import requests
from loguru import logger

class AntiCaptchaAdapter:
    """Adapter for Anti-Captcha service"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anti-captcha.com"
    
    def solve_recaptcha_v2(self, site_key: str, page_url: str) -> dict:
        """Solve reCAPTCHA v2"""
        try:
            # Create task
            task_data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": page_url,
                    "websiteKey": site_key
                }
            }
            
            response = requests.post(
                f"{self.base_url}/createTask",
                json=task_data,
                timeout=30
            )
            
            result = response.json()
            if result.get('errorId') != 0:
                return {'success': False, 'error': result.get('errorDescription')}
            
            task_id = result.get('taskId')
            
            # Wait for solution
            for _ in range(60):
                time.sleep(3)
                
                check_data = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                
                check_response = requests.post(
                    f"{self.base_url}/getTaskResult",
                    json=check_data,
                    timeout=30
                )
                
                check_result = check_response.json()
                
                if check_result.get('status') == 'ready':
                    solution = check_result.get('solution', {}).get('gRecaptchaResponse')
                    return {'success': True, 'code': solution}
            
            return {'success': False, 'error': 'Timeout'}
            
        except Exception as e:
            logger.error(f"Anti-Captcha error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_balance(self) -> float:
        """Get account balance"""
        try:
            response = requests.post(
                f"{self.base_url}/getBalance",
                json={"clientKey": self.api_key},
                timeout=10
            )
            
            result = response.json()
            if result.get('errorId') == 0:
                return result.get('balance', 0)
            return 0
            
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0
