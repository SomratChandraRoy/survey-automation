"""CAPTCHA solving with multiple FREE and paid options"""

import time
import os
import random
import traceback
from loguru import logger

class CaptchaSolver:
    """
    Universal CAPTCHA solver supporting:
    - FREE audio solver (Google Speech API)
    - FREE trial services
    - Paid services (2Captcha, etc.)
    - CAPTCHA avoidance
    """
    
    def __init__(self, settings, error_tracker=None):
        self.settings = settings
        self.error_tracker = error_tracker
        self.method = os.getenv('CAPTCHA_METHOD', 'audio_free')
        
        # Initialize appropriate solver
        try:
            if self.method == 'audio_free':
                from src.captcha.audio_solver import AudioCaptchaSolver
                self.audio_solver = AudioCaptchaSolver(settings, error_tracker)
                logger.info("🆓 Using FREE audio CAPTCHA solver (Google Speech API)")
            
            elif self.method == 'free_trial':
                from src.captcha.audio_solver import FreeTrialCaptchaSolver
                self.trial_solver = FreeTrialCaptchaSolver(settings, error_tracker)
                logger.info("🆓 Using FREE trial CAPTCHA services")
            
            elif self.method == '2captcha':
                try:
                    from twocaptcha import TwoCaptcha
                    api_key = getattr(settings, 'captcha_api_key', None)
                    if api_key and api_key != 'your_2captcha_api_key_here':
                        self.paid_solver = TwoCaptcha(api_key)
                        logger.info("💰 Using 2Captcha (paid service)")
                    else:
                        logger.warning("⚠️ 2Captcha API key not configured, falling back to FREE audio solver")
                        from src.captcha.audio_solver import AudioCaptchaSolver
                        self.audio_solver = AudioCaptchaSolver(settings, error_tracker)
                        self.method = 'audio_free'
                except ImportError:
                    logger.warning("⚠️ 2captcha-python not installed, using FREE audio solver")
                    from src.captcha.audio_solver import AudioCaptchaSolver
                    self.audio_solver = AudioCaptchaSolver(settings, error_tracker)
                    self.method = 'audio_free'
            
            elif self.method == 'avoid_only':
                logger.info("🛡️ CAPTCHA avoidance mode (no solving)")
            
            else:
                # Default to free audio solver
                from src.captcha.audio_solver import AudioCaptchaSolver
                self.audio_solver = AudioCaptchaSolver(settings, error_tracker)
                logger.info("🆓 Using FREE audio CAPTCHA solver (default)")
                self.method = 'audio_free'
                
        except Exception as e:
            error_msg = f"Failed to initialize CAPTCHA solver: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'initialization_failed', error_msg)
            # Fallback to avoid_only mode
            self.method = 'avoid_only'
            logger.warning("⚠️ Falling back to CAPTCHA avoidance mode")
    
    def solve_recaptcha_v2(self, site_key: str, page_url: str) -> dict:
        """Solve reCAPTCHA v2 using configured method"""
        logger.info(f"Solving reCAPTCHA v2 using method: {self.method}")
        
        try:
            if not site_key or not page_url:
                error_msg = f"Invalid parameters: site_key={site_key}, page_url={page_url}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('captcha', 'invalid_parameters', error_msg)
                return {'success': False, 'error': 'Invalid parameters'}
            
            if self.method == 'audio_free':
                # Use FREE audio solver
                return self.audio_solver.solve_recaptcha_audio(None)  # Driver passed separately
            
            elif self.method == 'free_trial':
                # Use FREE trial service
                return self.trial_solver.solve_captcha(site_key, page_url)
            
            elif self.method == '2captcha' and hasattr(self, 'paid_solver'):
                # Use paid 2Captcha service
                try:
                    result = self.paid_solver.recaptcha(
                        sitekey=site_key,
                        url=page_url
                    )
                    logger.info("✓ reCAPTCHA v2 solved with 2Captcha")
                    return {'success': True, 'code': result['code']}
                except Exception as e:
                    error_msg = f"2Captcha solve failed: {str(e)}"
                    logger.error(error_msg)
                    if self.error_tracker:
                        self.error_tracker.log_error('captcha', '2captcha_failed', error_msg)
                    return {'success': False, 'error': str(e)}
            
            elif self.method == 'avoid_only':
                # Just wait and hope CAPTCHA is avoided
                logger.info("Avoidance mode - waiting...")
                time.sleep(5)
                return {'success': True, 'code': None, 'message': 'Avoidance mode'}
            
            else:
                # Fallback to audio solver
                logger.warning("Falling back to FREE audio solver")
                if hasattr(self, 'audio_solver'):
                    return self.audio_solver.solve_recaptcha_audio(None)
                else:
                    return {'success': False, 'error': 'No solver available'}
                
        except Exception as e:
            error_msg = f"Failed to solve reCAPTCHA v2: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'solve_failed', error_msg)
            return {'success': False, 'error': str(e)}
    
    def solve_recaptcha_v3(self, site_key: str, page_url: str, action: str = 'verify') -> dict:
        """Solve reCAPTCHA v3"""
        logger.info("Solving reCAPTCHA v3...")
        
        try:
            result = self.solver.recaptcha(
                sitekey=site_key,
                url=page_url,
                version='v3',
                action=action,
                min_score=0.7
            )
            
            logger.info("reCAPTCHA v3 solved successfully")
            return {
                'success': True,
                'code': result['code']
            }
            
        except Exception as e:
            logger.error(f"Failed to solve reCAPTCHA v3: {e}")
            return {'success': False, 'error': str(e)}
    
    def solve_image_captcha(self, image_path: str) -> dict:
        """Solve image-based CAPTCHA"""
        logger.info("Solving image CAPTCHA...")
        
        try:
            result = self.solver.normal(image_path)
            
            logger.info("Image CAPTCHA solved successfully")
            return {
                'success': True,
                'code': result['code']
            }
            
        except Exception as e:
            logger.error(f"Failed to solve image CAPTCHA: {e}")
            return {'success': False, 'error': str(e)}
    
    def detect_and_solve(self, driver, page_url: str) -> dict:
        """Detect CAPTCHA type and solve automatically with human-like behavior"""
        logger.info("Detecting CAPTCHA type...")
        
        try:
            if not driver:
                error_msg = "Driver is None"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('captcha', 'no_driver', error_msg)
                return {'success': False, 'error': 'No driver provided'}
            
            # Humans pause when they see CAPTCHA
            time.sleep(random.uniform(1.0, 2.0))
            
            # Check for reCAPTCHA v2
            try:
                recaptcha_v2 = driver.find_elements('css selector', '.g-recaptcha')
                if recaptcha_v2:
                    site_key = recaptcha_v2[0].get_attribute('data-sitekey')
                    if site_key:
                        # Scroll to CAPTCHA
                        driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            recaptcha_v2[0]
                        )
                        time.sleep(random.uniform(0.5, 1.0))
                        
                        # Humans look at CAPTCHA before clicking
                        time.sleep(random.uniform(1.5, 2.5))
                        
                        return self.solve_recaptcha_v2(site_key, page_url)
            except Exception as e:
                logger.debug(f"reCAPTCHA v2 check failed: {e}")
            
            # Check for reCAPTCHA v3
            try:
                recaptcha_v3 = driver.find_elements('css selector', '[data-sitekey]')
                for element in recaptcha_v3:
                    site_key = element.get_attribute('data-sitekey')
                    if site_key and 'recaptcha' in element.get_attribute('class').lower():
                        # v3 is invisible, but still pause naturally
                        time.sleep(random.uniform(0.5, 1.0))
                        return self.solve_recaptcha_v3(site_key, page_url)
            except Exception as e:
                logger.debug(f"reCAPTCHA v3 check failed: {e}")
            
            # Check for hCaptcha
            try:
                hcaptcha = driver.find_elements('css selector', '.h-captcha')
                if hcaptcha:
                    site_key = hcaptcha[0].get_attribute('data-sitekey')
                    if site_key:
                        # Scroll to CAPTCHA
                        driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            hcaptcha[0]
                        )
                        time.sleep(random.uniform(0.5, 1.0))
                        
                        # Humans look at hCaptcha
                        time.sleep(random.uniform(1.5, 2.5))
                        
                        logger.info("hCaptcha detected, solving...")
                        result = self.solver.hcaptcha(sitekey=site_key, url=page_url)
                        
                        # Simulate time it takes humans to solve
                        time.sleep(random.uniform(3.0, 6.0))
                        
                        return {'success': True, 'code': result['code']}
            except Exception as e:
                logger.debug(f"hCaptcha check failed: {e}")
            
            logger.info("No CAPTCHA detected")
            return {'success': True, 'code': None, 'message': 'No CAPTCHA found'}
            
        except Exception as e:
            error_msg = f"CAPTCHA detection/solving error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'detection_failed', error_msg)
            return {'success': False, 'error': str(e)}
    
    def inject_captcha_solution(self, driver, solution_code: str, captcha_type: str = 'recaptcha_v2'):
        """Inject CAPTCHA solution into page with human-like timing"""
        try:
            # Humans take time to solve CAPTCHA
            # Simulate realistic solving time
            if captcha_type == 'recaptcha_v2':
                # reCAPTCHA v2 takes 3-8 seconds for humans
                time.sleep(random.uniform(3.0, 8.0))
                
                # Inject solution
                script = f"""
                document.getElementById('g-recaptcha-response').innerHTML = '{solution_code}';
                """
                driver.execute_script(script)
                
            elif captcha_type == 'recaptcha_v3':
                # v3 is faster (invisible)
                time.sleep(random.uniform(1.0, 2.0))
                
                # Inject solution
                script = f"""
                document.getElementById('g-recaptcha-response-data-action').innerHTML = '{solution_code}';
                """
                driver.execute_script(script)
            
            logger.info("CAPTCHA solution injected")
            
            # Small pause after injection (natural behavior)
            time.sleep(random.uniform(0.5, 1.0))
            
        except Exception as e:
            logger.error(f"Failed to inject CAPTCHA solution: {e}")
