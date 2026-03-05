"""Browser automation with stealth and AI integration"""

import time
import random
import json
import traceback
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from loguru import logger

from src.ai.ollama_client import OllamaClient
from src.proxy.manager import ProxyManager
from src.captcha.solver import CaptchaSolver
from src.automation.stealth import StealthBrowser
from src.automation.survey_handler import SurveyHandler
from src.automation.human_behavior import HumanBehavior

class BrowserAutomation:
    """Main browser automation controller"""
    
    def __init__(self, settings, error_tracker=None):
        self.settings = settings
        self.error_tracker = error_tracker
        self.driver = None
        self.ai_client = OllamaClient(settings, error_tracker)
        self.proxy_manager = ProxyManager(settings)
        self.captcha_solver = CaptchaSolver(settings, error_tracker)
        self.stealth = StealthBrowser(settings)
        self.survey_handler = None
        self.human_behavior = None
        self.stats = {
            'surveys_completed': 0,
            'surveys_failed': 0,
            'captchas_solved': 0,
            'start_time': datetime.now()
        }
    
    def run(self):
        """Main automation workflow with comprehensive error handling"""
        try:
            logger.info("=" * 60)
            logger.info("Starting automation workflow")
            logger.info("=" * 60)
            
            # Step 1: Validate proxy
            logger.info("Step 1/5: Validating proxy...")
            try:
                if not self.proxy_manager.validate_proxy():
                    logger.error("❌ Proxy validation failed - KILL SWITCH ACTIVATED")
                    logger.error("Proxy is not working or has IP leaks")
                    logger.error("Please check your proxy configuration in .env file")
                    return False
                logger.info("✅ Proxy validated successfully")
            except Exception as e:
                logger.error(f"❌ Proxy validation error: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            # Step 2: Initialize browser
            logger.info("Step 2/5: Initializing browser...")
            try:
                if not self.init_browser():
                    logger.error("❌ Browser initialization failed")
                    logger.error("Check if Chrome/Chromium is installed")
                    logger.error("Install: sudo apt-get install chromium-browser")
                    return False
                logger.info("✅ Browser initialized successfully")
            except Exception as e:
                logger.error(f"❌ Browser initialization error: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            # Step 3: Login
            logger.info("Step 3/5: Logging in...")
            try:
                if not self.login():
                    logger.error("❌ Login failed")
                    logger.error("Check your credentials in .env file")
                    logger.error("Or check if Opinion Edge website is accessible")
                    return False
                logger.info("✅ Login successful")
            except Exception as e:
                logger.error(f"❌ Login error: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            # Step 4: Navigate to surveys
            logger.info("Step 4/5: Navigating to surveys...")
            try:
                if not self.navigate_to_surveys():
                    logger.error("❌ Failed to navigate to surveys")
                    logger.error("Survey page may have changed or is unavailable")
                    return False
                logger.info("✅ Navigated to surveys successfully")
            except Exception as e:
                logger.error(f"❌ Navigation error: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            # Step 5: Process surveys
            logger.info("Step 5/5: Processing surveys...")
            try:
                self.process_surveys()
                logger.info("✅ Survey processing completed")
            except Exception as e:
                logger.error(f"❌ Survey processing error: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            logger.info("=" * 60)
            logger.info("✅ Automation workflow completed successfully")
            logger.info(f"   Surveys completed: {self.stats['surveys_completed']}")
            logger.info(f"   Surveys failed: {self.stats['surveys_failed']}")
            logger.info(f"   CAPTCHAs solved: {self.stats['captchas_solved']}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in automation workflow: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        finally:
            self.save_stats()
    
    def init_browser(self) -> bool:
        """Initialize browser with stealth settings and comprehensive error handling"""
        logger.info("Initializing browser...")
        
        try:
            # Check if Chrome/Chromium is available
            try:
                import shutil
                chrome_path = shutil.which('chromium-browser') or shutil.which('google-chrome') or shutil.which('chrome')
                if not chrome_path:
                    logger.error("Chrome/Chromium not found in PATH")
                    logger.error("Install: sudo apt-get install chromium-browser")
                    return False
                logger.debug(f"Found Chrome at: {chrome_path}")
            except Exception as e:
                logger.warning(f"Could not verify Chrome installation: {e}")
            
            options = uc.ChromeOptions()
            
            # Proxy configuration (optional)
            if self.settings.proxy_enabled:
                try:
                    proxy_url = self.settings.proxy_url
                    options.add_argument(f'--proxy-server={proxy_url}')
                    logger.debug(f"Proxy configured: {self.settings.proxy_host}:{self.settings.proxy_port}")
                except Exception as e:
                    logger.error(f"Failed to configure proxy: {e}")
                    return False
            else:
                logger.info("Running without proxy (direct connection)")
            
            # Stealth options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-webrtc')
            options.add_argument('--disable-webrtc-hw-encoding')
            options.add_argument('--disable-webrtc-encryption')
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Headless mode for server
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
            
            # Suppress logging
            options.add_argument('--log-level=3')
            options.add_argument('--silent')
            
            # Initialize driver
            logger.info("Starting Chrome driver...")
            try:
                self.driver = uc.Chrome(options=options, version_main=120)
                self.driver.set_page_load_timeout(30)
                logger.info("✅ Chrome driver started")
            except Exception as e:
                logger.error(f"Failed to start Chrome driver: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                logger.error("Try: pip install --upgrade undetected-chromedriver")
                return False
            
            # Apply stealth scripts
            try:
                self.stealth.apply_stealth(self.driver)
                logger.info("✅ Stealth configurations applied")
            except Exception as e:
                logger.error(f"Failed to apply stealth: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                # Continue anyway, stealth is optional
            
            # Initialize human behavior simulator
            try:
                self.human_behavior = HumanBehavior(self.driver, self.settings)
                logger.info("✅ Human behavior simulator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize human behavior: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            # Initialize survey handler
            try:
                self.survey_handler = SurveyHandler(self.driver, self.ai_client, self.settings, self.human_behavior, self.error_tracker)
                logger.info("✅ Survey handler initialized")
            except Exception as e:
                logger.error(f"Failed to initialize survey handler: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
            
            logger.info("✅ Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Browser initialization error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def login(self) -> bool:
        """Login to Opinion Edge with human-like behavior"""
        logger.info("Starting login process...")
        
        base_url = self.settings.opinion_edge_base_url.rstrip('/')

        try:
            # Check if we have valid cookies first
            if self.load_cookies():
                logger.info("Found existing cookies, attempting to reuse session...")
                self.driver.get(f'{base_url}/mySurvey')
                self.human_delay(3, 5)
                
                # Check if still logged in
                if 'mysurvey' in self.driver.current_url.lower() or 'dashboard' in self.driver.current_url.lower():
                    logger.info("✅ Session restored from cookies - skipping login")
                    return True
                else:
                    logger.info("Cookies expired, proceeding with login...")
            
            # Navigate to homepage
            self.driver.get(f'{base_url}/')
            
            # Simulate human page scan
            self.human_behavior.simulate_page_scan()
            
            # Take screenshot for AI analysis
            screenshot_path = self.take_screenshot('login_page')
            
            # Detect CAPTCHA
            captcha_result = self.ai_client.detect_captcha(screenshot_path)
            if captcha_result.get('captcha_present'):
                logger.info(f"CAPTCHA detected: {captcha_result.get('captcha_type')}")
                self.human_behavior.simulate_captcha_solving_behavior()
                if not self.handle_captcha():
                    return False
            
            # Find and click login button using AI
            button_coords = self.ai_client.extract_button_coordinates(screenshot_path)
            if button_coords.get('button_found'):
                # Simulate reading/thinking before clicking
                self.human_behavior.simulate_thinking('simple')
                
                self.click_at_coordinates(
                    button_coords.get('x_percent', 50),
                    button_coords.get('y_percent', 50)
                )
                self.human_delay()
            else:
                # Fallback: try to find login button by common selectors
                login_selectors = [
                    "//button[contains(text(), 'Login')]",
                    "//a[contains(text(), 'Login')]",
                    "//button[contains(@class, 'login')]",
                    "#login-button"
                ]
                
                for selector in login_selectors:
                    try:
                        if selector.startswith('//'):
                            element = self.driver.find_element(By.XPATH, selector)
                        else:
                            element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        # Human behavior before clicking
                        self.human_behavior.natural_mouse_move_to_element(element)
                        self.human_click(element)
                        break
                    except:
                        continue
            
            self.human_delay()
            
            # Simulate form filling behavior
            self.human_behavior.simulate_form_filling_behavior()
            
            # Enter credentials with human-like typing
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            
            # Humans often click field first, then pause
            self.human_behavior.natural_mouse_move_to_element(email_field)
            time.sleep(random.uniform(0.3, 0.7))
            
            self.human_type(email_field, self.settings.opinion_edge_email)
            
            # Small pause between fields (natural behavior)
            time.sleep(random.uniform(0.5, 1.2))
            
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
            self.human_type(password_field, self.settings.opinion_edge_password)
            
            # Humans often review what they typed
            self.human_delay(1, 2)
            
            # Check for CAPTCHA again
            screenshot_path = self.take_screenshot('before_submit')
            captcha_result = self.ai_client.detect_captcha(screenshot_path)
            if captcha_result.get('captcha_present'):
                self.human_behavior.simulate_captcha_solving_behavior()
                if not self.handle_captcha():
                    return False
            
            # Submit login with human hesitation
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            
            # Humans often pause before final submit
            time.sleep(random.uniform(0.8, 1.5))
            
            self.human_click(submit_button)
            
            # Wait for page load with human-like patience
            self.human_delay(5, 8)
            
            # Verify login success
            if 'dashboard' in self.driver.current_url.lower() or 'mysurvey' in self.driver.current_url.lower():
                logger.info("Login successful")
                self.save_cookies()
                
                # Humans scan the page after login
                self.human_behavior.simulate_page_scan()
                
                return True
            else:
                logger.warning("Login may have failed - checking page state")
                screenshot_path = self.take_screenshot('after_login')
                return True  # Continue anyway
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def handle_captcha(self) -> bool:
        """Handle CAPTCHA with retry logic"""
        max_attempts = 3
        
        for attempt in range(max_attempts):
            logger.info(f"CAPTCHA solving attempt {attempt + 1}/{max_attempts}")
            
            try:
                result = self.captcha_solver.detect_and_solve(
                    self.driver,
                    self.driver.current_url
                )
                
                if result.get('success') and result.get('code'):
                    # Inject solution
                    self.captcha_solver.inject_captcha_solution(
                        self.driver,
                        result['code']
                    )
                    self.stats['captchas_solved'] += 1
                    logger.info("CAPTCHA solved successfully")
                    return True
                    
            except Exception as e:
                logger.error(f"CAPTCHA solving error: {e}")
            
            self.human_delay(2, 4)
        
        logger.error("Failed to solve CAPTCHA after all attempts")
        return False
    
    def navigate_to_surveys(self) -> bool:
        """Navigate to survey page"""
        logger.info("Navigating to surveys...")
        
        base_url = self.settings.opinion_edge_base_url.rstrip('/')

        try:
            self.driver.get(f'{base_url}/mySurvey')
            self.human_delay()
            
            # Wait for page load
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            self.take_screenshot('survey_page')
            logger.info("Successfully navigated to surveys")
            return True
            
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False
    
    def process_surveys(self):
        """Process available surveys with rate limiting and earnings tracking"""
        logger.info("Processing surveys...")
        
        try:
            # Check if surveys are available
            if not self._check_surveys_available():
                logger.info("ℹ️ No surveys available at this time")
                logger.info("💡 Tip: Surveys are usually available during peak hours (9AM-12PM, 6PM-9PM)")
                return
            
            surveys_processed = 0
            max_surveys = 10  # Process up to 10 surveys per session
            
            # Load daily limit tracker
            daily_limit = self._check_daily_limit()
            if daily_limit >= 20:
                logger.warning("⚠️ Daily survey limit reached (20 surveys)")
                logger.info("💡 Tip: Wait until tomorrow to avoid detection")
                return
            
            while surveys_processed < max_surveys:
                # Find available surveys
                survey_links = self.find_survey_links()
                
                if not survey_links:
                    logger.info("No more surveys available")
                    break
                
                for survey_link in survey_links[:3]:  # Process 3 at a time
                    # Rate limiting - minimum 2 minutes between surveys
                    if surveys_processed > 0:
                        wait_time = random.randint(120, 180)
                        logger.info(f"⏳ Rate limiting: waiting {wait_time}s before next survey...")
                        time.sleep(wait_time)
                    
                    # Process survey
                    start_time = time.time()
                    success = self.survey_handler.process_survey(survey_link)
                    duration = time.time() - start_time
                    
                    if success:
                        self.stats['surveys_completed'] += 1
                        surveys_processed += 1
                        
                        # Track earnings (estimate $1.50 per survey)
                        self._track_earnings(1.50, duration)
                        
                        logger.info(f"✅ Survey completed in {duration:.0f}s")
                        logger.info(f"💰 Estimated earnings: +$1.50")
                    else:
                        self.stats['surveys_failed'] += 1
                        logger.warning(f"❌ Survey failed")
                    
                    # Update daily limit
                    self._update_daily_limit()
                    
                    self.human_delay(10, 20)
                    
                    if surveys_processed >= max_surveys:
                        break
                
                # Return to survey list
                self.driver.get(f"{self.settings.opinion_edge_base_url.rstrip('/')}/mySurvey")
                self.human_delay()
            
            logger.info(f"✅ Processed {surveys_processed} surveys")
            logger.info(f"💰 Session earnings: ${surveys_processed * 1.50:.2f}")
            
        except Exception as e:
            logger.error(f"Survey processing error: {e}")
    
    def _check_surveys_available(self) -> bool:
        """Check if surveys are actually available"""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            
            # Check for "no surveys" messages
            no_survey_indicators = [
                'no surveys available',
                'no surveys at this time',
                'check back later',
                'keine umfragen',
                'currently no surveys'
            ]
            
            for indicator in no_survey_indicators:
                if indicator in page_text:
                    return False
            
            # Check if survey links exist
            survey_links = self.find_survey_links()
            return len(survey_links) > 0
            
        except Exception as e:
            logger.error(f"Error checking survey availability: {e}")
            return True  # Assume available if check fails
    
    def _check_daily_limit(self) -> int:
        """Check how many surveys completed today"""
        try:
            limit_file = self.settings.data_dir / 'daily_limit.json'
            if limit_file.exists():
                import json
                from datetime import datetime
                
                with open(limit_file, 'r') as f:
                    data = json.load(f)
                
                # Check if it's a new day
                today = datetime.now().strftime('%Y-%m-%d')
                if data.get('date') == today:
                    return data.get('count', 0)
            
            return 0
        except Exception as e:
            logger.error(f"Error checking daily limit: {e}")
            return 0
    
    def _update_daily_limit(self):
        """Update daily survey count"""
        try:
            import json
            from datetime import datetime
            
            limit_file = self.settings.data_dir / 'daily_limit.json'
            today = datetime.now().strftime('%Y-%m-%d')
            
            if limit_file.exists():
                with open(limit_file, 'r') as f:
                    data = json.load(f)
                
                if data.get('date') == today:
                    data['count'] = data.get('count', 0) + 1
                else:
                    data = {'date': today, 'count': 1}
            else:
                data = {'date': today, 'count': 1}
            
            with open(limit_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error updating daily limit: {e}")
    
    def _track_earnings(self, amount: float, duration: float):
        """Track earnings from completed survey with accurate period calculations"""
        try:
            import json
            from datetime import datetime, timedelta

            earnings_file = self.settings.data_dir / 'earnings.json'

            now = datetime.now()
            today_str = now.strftime('%Y-%m-%d')
            week_str = now.strftime('%Y-W%W')
            month_str = now.strftime('%Y-%m')

            if earnings_file.exists():
                with open(earnings_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {
                    'total_earnings': 0,
                    'surveys_completed': 0,
                    'average_per_survey': 0,
                    'periods': {},
                    'last_updated': None
                }

            # Ensure periods dict exists (migrate old format)
            if 'periods' not in data:
                data['periods'] = {}

            # Update period totals
            for key in (today_str, week_str, month_str):
                if key not in data['periods']:
                    data['periods'][key] = {'earnings': 0, 'surveys': 0}
                data['periods'][key]['earnings'] += amount
                data['periods'][key]['surveys'] += 1

            # Update overall totals
            data['total_earnings'] = data.get('total_earnings', 0) + amount
            data['surveys_completed'] = data.get('surveys_completed', 0) + 1
            data['average_per_survey'] = (
                data['total_earnings'] / data['surveys_completed']
            )

            # Convenience fields for dashboard
            data['today_earnings'] = data['periods'].get(today_str, {}).get('earnings', 0)
            data['this_week_earnings'] = data['periods'].get(week_str, {}).get('earnings', 0)
            data['this_month_earnings'] = data['periods'].get(month_str, {}).get('earnings', 0)
            data['last_updated'] = now.isoformat()

            with open(earnings_file, 'w') as f:
                json.dump(data, f, indent=2)

            logger.debug(f"Earnings tracked: ${amount:.2f}")
            
        except Exception as e:
            logger.error(f"Error tracking earnings: {e}")
    
    def find_survey_links(self) -> list:
        """Find available survey links"""
        try:
            # Common selectors for survey links
            selectors = [
                "a[href*='survey']",
                ".survey-link",
                "[data-survey-id]",
                "button[onclick*='survey']"
            ]
            
            links = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    links.extend([elem.get_attribute('href') or elem.get_attribute('onclick') for elem in elements])
                except:
                    continue
            
            return [link for link in links if link]
            
        except Exception as e:
            logger.error(f"Error finding survey links: {e}")
            return []
    
    def take_screenshot(self, name: str) -> Path:
        """Take screenshot and return path"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = self.settings.screenshots_dir / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            return filepath
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return None
    
    def human_delay(self, min_sec: int = None, max_sec: int = None):
        """Random delay to mimic human behavior with realistic patterns"""
        min_sec = min_sec or self.settings.action_delay_min
        max_sec = max_sec or self.settings.action_delay_max
        
        # Add realistic variation - humans don't have uniform delays
        # Use beta distribution for more realistic timing
        alpha, beta = 2, 5  # Skewed towards faster but with occasional pauses
        normalized = random.betavariate(alpha, beta)
        delay = min_sec + (max_sec - min_sec) * normalized
        
        # Occasionally add extra "thinking" time (10% chance)
        if random.random() < 0.1:
            delay += random.uniform(1, 3)
        
        time.sleep(delay)
    
    def human_click(self, element):
        """Click with human-like mouse movement and behavior"""
        try:
            # Scroll element into view naturally
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.3, 0.7))
            
            # Get element location
            location = element.location
            size = element.size
            
            # Move mouse in a curved path (Bezier curve simulation)
            actions = ActionChains(self.driver)
            
            # Add slight overshoot and correction (humans rarely click perfectly first time)
            if random.random() < 0.3:  # 30% chance of slight overshoot
                overshoot_x = random.randint(-5, 5)
                overshoot_y = random.randint(-5, 5)
                actions.move_to_element_with_offset(element, overshoot_x, overshoot_y)
                actions.pause(random.uniform(0.05, 0.15))
            
            # Move to element with slight randomness (humans don't click exact center)
            offset_x = random.randint(-size['width']//4, size['width']//4)
            offset_y = random.randint(-size['height']//4, size['height']//4)
            actions.move_to_element_with_offset(element, offset_x, offset_y)
            
            # Pause before click (human reaction time)
            actions.pause(random.uniform(0.15, 0.35))
            
            # Sometimes double-check by hovering (5% chance)
            if random.random() < 0.05:
                actions.pause(random.uniform(0.2, 0.5))
            
            actions.click()
            actions.perform()
            
            # Small delay after click (human processing time)
            time.sleep(random.uniform(0.1, 0.3))
            
        except Exception as e:
            logger.warning(f"Human click failed, using direct click: {e}")
            element.click()
    
    def human_type(self, element, text: str):
        """Type with realistic human-like patterns"""
        # Click and focus
        self.human_click(element)
        time.sleep(random.uniform(0.2, 0.4))
        
        # Clear field naturally (humans often select all first)
        if random.random() < 0.7:  # 70% chance to select all first
            element.send_keys(Keys.CONTROL + "a")
            time.sleep(random.uniform(0.1, 0.2))
        
        # Type with realistic patterns
        for i, char in enumerate(text):
            element.send_keys(char)
            
            # Variable typing speed
            if char == ' ':
                # Longer pause after space (word boundary)
                delay = random.uniform(0.15, 0.35)
            elif char.isupper() or char in '!@#$%^&*()':
                # Slightly longer for special chars
                delay = random.uniform(0.12, 0.25)
            else:
                # Normal typing speed with variation
                base_speed = random.uniform(0.08, 0.18)
                # Typing gets slightly faster as you continue (muscle memory)
                speed_factor = max(0.7, 1 - (i / len(text)) * 0.3)
                delay = base_speed * speed_factor
            
            # Occasional typo and correction (5% chance)
            if random.random() < 0.05 and i < len(text) - 1:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(Keys.BACK_SPACE)
                time.sleep(random.uniform(0.1, 0.2))
            
            # Occasional pause (thinking/reading - 8% chance)
            if random.random() < 0.08:
                delay += random.uniform(0.3, 0.8)
            
            time.sleep(delay)
        
        # Small pause after typing (human verification)
        time.sleep(random.uniform(0.3, 0.7))
    
    def click_at_coordinates(self, x_percent: float, y_percent: float):
        """Click at specific coordinates"""
        try:
            size = self.driver.get_window_size()
            x = int(size['width'] * x_percent / 100)
            y = int(size['height'] * y_percent / 100)
            
            actions = ActionChains(self.driver)
            actions.move_by_offset(x, y)
            actions.click()
            actions.perform()
        except Exception as e:
            logger.error(f"Click at coordinates error: {e}")
    
    def save_cookies(self):
        """Save session cookies"""
        try:
            cookies = self.driver.get_cookies()
            cookie_file = self.settings.cookies_dir / 'session.json'
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f)
            logger.info("Cookies saved")
        except Exception as e:
            logger.error(f"Error saving cookies: {e}")
    
    def load_cookies(self):
        """Load session cookies"""
        try:
            cookie_file = self.settings.cookies_dir / 'session.json'
            if cookie_file.exists():
                # Check cookie age (expire after 7 days)
                import os
                from datetime import datetime, timedelta
                
                file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cookie_file))
                if file_age > timedelta(days=7):
                    logger.info("Cookies are too old (>7 days), will re-login")
                    return False
                
                # Navigate to domain first (required for setting cookies)
                self.driver.get('https://opinion-edge.com/')
                time.sleep(2)
                
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                
                for cookie in cookies:
                    try:
                        # Remove problematic fields
                        cookie.pop('sameSite', None)
                        cookie.pop('expiry', None)
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        logger.debug(f"Could not add cookie: {e}")
                
                logger.info("✅ Cookies loaded successfully")
                return True
        except Exception as e:
            logger.error(f"Error loading cookies: {e}")
        return False
    
    def save_stats(self):
        """Save automation statistics with performance metrics"""
        try:
            # Calculate performance metrics
            total_surveys = self.stats['surveys_completed'] + self.stats['surveys_failed']
            success_rate = (self.stats['surveys_completed'] / total_surveys * 100) if total_surveys > 0 else 0
            
            # Calculate earnings per hour
            duration_hours = (datetime.now() - self.stats['start_time']).total_seconds() / 3600
            earnings_per_hour = (self.stats['surveys_completed'] * 1.50) / duration_hours if duration_hours > 0 else 0
            
            # Average time per survey (estimate)
            avg_time_per_survey = (duration_hours * 3600) / self.stats['surveys_completed'] if self.stats['surveys_completed'] > 0 else 0
            
            stats_file = self.settings.data_dir / 'stats.json'
            with open(stats_file, 'w') as f:
                json.dump({
                    **self.stats,
                    'start_time': self.stats['start_time'].isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'success_rate': round(success_rate, 1),
                    'earnings_per_hour': round(earnings_per_hour, 2),
                    'average_time_per_survey': round(avg_time_per_survey, 0)
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving stats: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up browser resources...")
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
