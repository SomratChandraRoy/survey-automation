"""Advanced human behavior simulation"""

import time
import random
import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from loguru import logger

class HumanBehavior:
    """Simulate realistic human behavior patterns"""
    
    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings
        self.reading_speed_wpm = random.randint(200, 300)  # Words per minute
        self.session_start = time.time()
        self.actions_count = 0
        self.last_action_time = time.time()
    
    def simulate_reading(self, text: str):
        """Simulate time taken to read text"""
        if not text:
            return
        
        word_count = len(text.split())
        # Calculate reading time in seconds
        reading_time = (word_count / self.reading_speed_wpm) * 60
        
        # Add variation (humans don't read at constant speed)
        variation = random.uniform(0.8, 1.3)
        reading_time *= variation
        
        # Minimum reading time (even for short text)
        reading_time = max(reading_time, 1.5)
        
        logger.debug(f"Simulating reading {word_count} words (~{reading_time:.1f}s)")
        time.sleep(reading_time)
    
    def simulate_thinking(self, complexity: str = 'medium'):
        """Simulate thinking/decision time"""
        thinking_times = {
            'simple': (0.5, 1.5),
            'medium': (1.5, 3.5),
            'complex': (3.0, 6.0)
        }
        
        min_time, max_time = thinking_times.get(complexity, (1.5, 3.5))
        thinking_time = random.uniform(min_time, max_time)
        
        logger.debug(f"Simulating {complexity} thinking (~{thinking_time:.1f}s)")
        time.sleep(thinking_time)
    
    def random_mouse_movement(self):
        """Perform random mouse movements (humans move mouse while reading)"""
        if random.random() < 0.3:  # 30% chance
            try:
                actions = ActionChains(self.driver)
                
                # Random small movements
                for _ in range(random.randint(1, 3)):
                    x_offset = random.randint(-100, 100)
                    y_offset = random.randint(-50, 50)
                    actions.move_by_offset(x_offset, y_offset)
                    actions.pause(random.uniform(0.1, 0.3))
                
                actions.perform()
            except Exception as e:
                logger.debug(f"Random mouse movement failed: {e}")
    
    def random_scroll(self):
        """Perform random scrolling (humans scroll while reading)"""
        if random.random() < 0.4:  # 40% chance
            try:
                scroll_amount = random.randint(100, 400)
                direction = random.choice([1, -1])
                
                self.driver.execute_script(
                    f"window.scrollBy(0, {scroll_amount * direction});"
                )
                time.sleep(random.uniform(0.3, 0.7))
            except Exception as e:
                logger.debug(f"Random scroll failed: {e}")
    
    def simulate_page_scan(self):
        """Simulate scanning the page before interacting"""
        logger.debug("Simulating page scan")
        
        # Scroll to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.3, 0.6))
        
        # Scroll down in chunks (reading pattern)
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        
        current_position = 0
        while current_position < page_height:
            scroll_amount = random.randint(
                int(viewport_height * 0.3),
                int(viewport_height * 0.7)
            )
            current_position += scroll_amount
            
            self.driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(random.uniform(0.5, 1.2))
            
            # Random mouse movement while scrolling
            self.random_mouse_movement()
            
            # Don't scroll past the bottom
            if current_position >= page_height - viewport_height:
                break
    
    def simulate_form_filling_behavior(self):
        """Simulate realistic form filling patterns"""
        # Humans often pause before filling forms
        if random.random() < 0.6:
            time.sleep(random.uniform(0.5, 1.5))
        
        # Sometimes move mouse to form area first
        if random.random() < 0.4:
            self.random_mouse_movement()
    
    def simulate_decision_making(self, options_count: int):
        """Simulate time to make a decision among options"""
        # More options = more time to decide
        base_time = 1.5
        option_time = 0.5 * options_count
        total_time = base_time + option_time
        
        # Add variation
        total_time *= random.uniform(0.7, 1.3)
        
        logger.debug(f"Simulating decision among {options_count} options (~{total_time:.1f}s)")
        time.sleep(total_time)
    
    def check_fatigue(self):
        """Simulate human fatigue (slower actions over time)"""
        session_duration = time.time() - self.session_start
        
        # After 30 minutes, start slowing down
        if session_duration > 1800:
            fatigue_factor = 1 + ((session_duration - 1800) / 3600) * 0.3
            return min(fatigue_factor, 1.5)  # Max 50% slower
        
        return 1.0
    
    def take_micro_break(self):
        """Simulate micro-breaks (humans pause occasionally)"""
        self.actions_count += 1
        
        # Every 10-15 actions, take a small break
        if self.actions_count % random.randint(10, 15) == 0:
            break_time = random.uniform(2, 5)
            logger.debug(f"Taking micro-break ({break_time:.1f}s)")
            time.sleep(break_time)
            
            # Reset action counter with some randomness
            self.actions_count = random.randint(0, 3)
    
    def simulate_captcha_solving_behavior(self):
        """Simulate human behavior when solving CAPTCHA"""
        logger.debug("Simulating CAPTCHA solving behavior")
        
        # Humans pause when they see CAPTCHA
        time.sleep(random.uniform(1.0, 2.5))
        
        # Look at CAPTCHA (scroll to it)
        try:
            captcha_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                'iframe[src*="recaptcha"], .g-recaptcha, .h-captcha'
            )
            if captcha_elements:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    captcha_elements[0]
                )
                time.sleep(random.uniform(0.5, 1.0))
        except:
            pass
        
        # Humans often move mouse around CAPTCHA
        self.random_mouse_movement()
        
        # Pause before clicking (reading instructions)
        time.sleep(random.uniform(1.5, 3.0))
    
    def simulate_error_reaction(self):
        """Simulate human reaction to errors"""
        logger.debug("Simulating error reaction")
        
        # Humans pause when they see errors
        time.sleep(random.uniform(1.5, 3.0))
        
        # Might scroll to see full error
        self.random_scroll()
        
        # Read error message
        time.sleep(random.uniform(2.0, 4.0))
    
    def bezier_curve_mouse_movement(self, start_x, start_y, end_x, end_y, steps=20):
        """Generate points along a Bezier curve for realistic mouse movement"""
        # Control points for curve (adds natural arc to movement)
        ctrl1_x = start_x + (end_x - start_x) * random.uniform(0.2, 0.4)
        ctrl1_y = start_y + random.randint(-100, 100)
        ctrl2_x = start_x + (end_x - start_x) * random.uniform(0.6, 0.8)
        ctrl2_y = end_y + random.randint(-100, 100)
        
        points = []
        for i in range(steps):
            t = i / steps
            
            # Cubic Bezier curve formula
            x = (1-t)**3 * start_x + \
                3 * (1-t)**2 * t * ctrl1_x + \
                3 * (1-t) * t**2 * ctrl2_x + \
                t**3 * end_x
            
            y = (1-t)**3 * start_y + \
                3 * (1-t)**2 * t * ctrl1_y + \
                3 * (1-t) * t**2 * ctrl2_y + \
                t**3 * end_y
            
            points.append((int(x), int(y)))
        
        return points
    
    def natural_mouse_move_to_element(self, element):
        """Move mouse to element using natural curved path"""
        try:
            # Get current mouse position (approximate)
            current_x = random.randint(0, 800)
            current_y = random.randint(0, 600)
            
            # Get target element position
            location = element.location
            size = element.size
            target_x = location['x'] + size['width'] // 2
            target_y = location['y'] + size['height'] // 2
            
            # Generate curved path
            points = self.bezier_curve_mouse_movement(
                current_x, current_y,
                target_x, target_y,
                steps=random.randint(15, 25)
            )
            
            # Move along path
            actions = ActionChains(self.driver)
            for i, (x, y) in enumerate(points):
                if i > 0:
                    prev_x, prev_y = points[i-1]
                    actions.move_by_offset(x - prev_x, y - prev_y)
                    
                    # Variable speed (faster in middle, slower at start/end)
                    if i < 5 or i > len(points) - 5:
                        actions.pause(random.uniform(0.01, 0.03))
                    else:
                        actions.pause(random.uniform(0.005, 0.015))
            
            actions.perform()
            
        except Exception as e:
            logger.debug(f"Natural mouse movement failed: {e}")
    
    def simulate_survey_start_behavior(self):
        """Simulate behavior when starting a survey"""
        logger.debug("Simulating survey start behavior")
        
        # Scan the page first
        self.simulate_page_scan()
        
        # Read instructions/title
        time.sleep(random.uniform(2.0, 4.0))
        
        # Small pause before starting
        time.sleep(random.uniform(1.0, 2.0))
    
    def simulate_survey_completion_behavior(self):
        """Simulate behavior when completing a survey"""
        logger.debug("Simulating survey completion behavior")
        
        # Humans often review before final submit
        if random.random() < 0.4:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1.0, 2.0))
            self.random_scroll()
        
        # Pause before final submit
        time.sleep(random.uniform(1.5, 3.0))
    
    def add_human_noise(self):
        """Add random human-like noise to actions"""
        noise_actions = [
            self.random_mouse_movement,
            self.random_scroll,
            lambda: time.sleep(random.uniform(0.5, 1.5))
        ]
        
        if random.random() < 0.2:  # 20% chance
            random.choice(noise_actions)()
