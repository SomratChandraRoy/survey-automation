"""Survey question handling and answering"""

import time
import random
import traceback
from datetime import datetime
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, StaleElementReferenceException,
    WebDriverException
)
from loguru import logger

class SurveyHandler:
    """Handle survey questions and answers"""
    
    def __init__(self, driver, ai_client, settings, human_behavior, error_tracker=None):
        self.driver = driver
        self.ai_client = ai_client
        self.settings = settings
        self.human_behavior = human_behavior
        self.error_tracker = error_tracker
        self.knowledge_base = self.load_knowledge_base()
    
    def load_knowledge_base(self) -> dict:
        """Load pre-defined answers"""
        return {
            'age': str(self.settings.persona_age),
            'birthday': self.settings.persona_birthday,
            'birth_year': '1963',
            'name': self.settings.persona_name,
            'address': self.settings.persona_address,
            'phone': self.settings.persona_phone,
            'country': 'Germany',
            'language': 'German',
            'gender': 'Male',
            'occupation': 'Retired',
            # Trap questions
            'on_the_moon': 'No',
            'can_fly': 'No',
            'breathing_underwater': 'No'
        }
    
    def process_survey(self, survey_url: str) -> bool:
        """Process a single survey with human-like behavior"""
        logger.info(f"Processing survey: {survey_url}")
        
        try:
            # Navigate to survey
            if not survey_url or not isinstance(survey_url, str):
                error_msg = f"Invalid survey URL: {survey_url}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('survey', 'invalid_url', error_msg)
                return False
            
            if survey_url.startswith('http'):
                try:
                    self.driver.get(survey_url)
                    logger.info(f"✓ Navigated to survey: {survey_url[:50]}...")
                except WebDriverException as e:
                    error_msg = f"Failed to navigate to survey: {str(e)}"
                    logger.error(error_msg)
                    if self.error_tracker:
                        self.error_tracker.log_error('survey', 'navigation_failed', error_msg)
                    return False
            else:
                # Handle onclick or relative URLs
                logger.warning("Non-standard survey URL, skipping")
                if self.error_tracker:
                    self.error_tracker.log_error('survey', 'non_standard_url', f"URL: {survey_url}")
                return False
            
            # Simulate human survey start behavior
            self.human_behavior.simulate_survey_start_behavior()
            
            # Process questions in loop
            questions_answered = 0
            max_questions = 50
            
            while questions_answered < max_questions:
                # Check if survey is complete
                if self.is_survey_complete():
                    logger.info("Survey completed successfully")
                    
                    # Human behavior at completion
                    self.human_behavior.simulate_survey_completion_behavior()
                    
                    self.save_survey_result(survey_url, True, questions_answered)
                    return True
                
                # Take screenshot
                try:
                    screenshot_path = self.take_screenshot(f'question_{questions_answered}')
                except Exception as e:
                    logger.warning(f"Screenshot failed: {e}")
                    screenshot_path = None
                
                # Get question text
                try:
                    question_text = self.extract_question_text()
                except Exception as e:
                    logger.error(f"Failed to extract question text: {e}")
                    if self.error_tracker:
                        self.error_tracker.log_error('survey', 'question_extraction_failed', str(e))
                    question_text = ""
                
                # Simulate reading the question
                if question_text:
                    self.human_behavior.simulate_reading(question_text)
                
                # Check knowledge base first
                answer = self.check_knowledge_base(question_text)
                
                if not answer:
                    # Use AI to generate answer
                    # Simulate thinking before AI call
                    self.human_behavior.simulate_thinking('medium')
                    
                    try:
                        ai_response = self.ai_client.answer_survey_question(
                            screenshot_path,
                            question_text
                        )
                        answer = ai_response.get('answer', '')
                        answer_type = ai_response.get('answer_type', 'text')
                        
                        if not answer:
                            logger.warning("AI returned empty answer, using fallback")
                            answer = "No answer"
                            
                    except Exception as e:
                        error_msg = f"AI answer generation failed: {str(e)}"
                        logger.error(error_msg)
                        if self.error_tracker:
                            self.error_tracker.log_error('ai', 'answer_generation_failed', error_msg)
                        # Use fallback answer
                        answer = "No answer"
                        answer_type = 'text'
                else:
                    answer_type = 'text'
                    # Quick decision for known answers
                    self.human_behavior.simulate_thinking('simple')
                
                # Submit answer with human behavior
                if self.submit_answer(answer, answer_type):
                    questions_answered += 1
                    logger.info(f"Question {questions_answered} answered: {answer[:50]}")
                    
                    # Take micro-break occasionally
                    self.human_behavior.take_micro_break()
                else:
                    logger.warning("Failed to submit answer")
                
                # Human-like delay between questions
                fatigue_factor = self.human_behavior.check_fatigue()
                base_delay = random.uniform(2, 4)
                time.sleep(base_delay * fatigue_factor)
                
                # Random human noise
                self.human_behavior.add_human_noise()
                
                # Check for errors
                if self.check_for_errors():
                    logger.error("Error detected in survey")
                    self.human_behavior.simulate_error_reaction()
                    break
            
            logger.warning("Survey reached max questions without completion")
            self.save_survey_result(survey_url, False, questions_answered)
            return False
            
        except Exception as e:
            error_msg = f"Survey processing error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('survey', 'processing_failed', error_msg)
            
            try:
                self.save_survey_result(survey_url, False, 0)
            except:
                pass
            
            return False
    
    def extract_question_text(self) -> str:
        """Extract question text from page"""
        try:
            # Common question selectors
            selectors = [
                '.question-text',
                '.survey-question',
                'h2',
                'h3',
                '[role="heading"]',
                'label'
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        text = ' '.join([elem.text for elem in elements if elem.text])
                        if text:
                            return text[:500]  # Limit length
                except (NoSuchElementException, StaleElementReferenceException):
                    continue
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            logger.debug("No question text found with standard selectors")
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting question: {e}")
            if self.error_tracker:
                self.error_tracker.log_error('survey', 'question_extraction_error', str(e))
            return ""
    
    def check_knowledge_base(self, question_text: str) -> str:
        """Check if we have a pre-defined answer"""
        question_lower = question_text.lower()
        
        # Age questions
        if any(word in question_lower for word in ['age', 'alt', 'jahre']):
            return self.knowledge_base['age']
        
        # Birthday questions
        if any(word in question_lower for word in ['birthday', 'geburtsdatum', 'birth']):
            return self.knowledge_base['birthday']
        
        # Name questions
        if any(word in question_lower for word in ['name', 'namen']):
            return self.knowledge_base['name']
        
        # Trap questions
        if 'moon' in question_lower or 'mond' in question_lower:
            return 'No'
        
        if 'fly' in question_lower or 'fliegen' in question_lower:
            return 'No'
        
        return None
    
    def submit_answer(self, answer: str, answer_type: str) -> bool:
        """Submit answer based on type"""
        try:
            if answer_type == 'radio':
                return self.select_radio_option(answer)
            elif answer_type == 'checkbox':
                return self.select_checkbox_option(answer)
            else:
                return self.enter_text_answer(answer)
                
        except Exception as e:
            logger.error(f"Error submitting answer: {e}")
            return False
    
    def enter_text_answer(self, answer: str) -> bool:
        """Enter text answer with human-like typing"""
        try:
            if not answer:
                logger.warning("Empty answer provided")
                return False
            
            # Find text input
            try:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='text'], textarea, input:not([type='radio']):not([type='checkbox'])")
            except Exception as e:
                logger.error(f"Failed to find input elements: {e}")
                if self.error_tracker:
                    self.error_tracker.log_error('survey', 'input_not_found', str(e))
                return False
            
            if inputs:
                input_field = inputs[0]
                
                # Scroll to input
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    input_field
                )
                time.sleep(random.uniform(0.3, 0.6))
                
                # Click field (humans click before typing)
                self.human_behavior.natural_mouse_move_to_element(input_field)
                input_field.click()
                time.sleep(random.uniform(0.2, 0.5))
                
                # Clear field naturally
                if random.random() < 0.7:
                    input_field.send_keys(Keys.CONTROL + "a")
                    time.sleep(random.uniform(0.1, 0.2))
                
                # Type with realistic human patterns
                for i, char in enumerate(answer):
                    input_field.send_keys(char)
                    
                    # Variable typing speed
                    if char == ' ':
                        delay = random.uniform(0.15, 0.35)
                    elif char.isupper() or char in '!@#$%^&*()':
                        delay = random.uniform(0.12, 0.25)
                    else:
                        base_speed = random.uniform(0.08, 0.18)
                        speed_factor = max(0.7, 1 - (i / len(answer)) * 0.3)
                        delay = base_speed * speed_factor
                    
                    # Occasional typo (3% chance)
                    if random.random() < 0.03 and i < len(answer) - 1:
                        wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                        input_field.send_keys(wrong_char)
                        time.sleep(random.uniform(0.1, 0.2))
                        input_field.send_keys(Keys.BACK_SPACE)
                        time.sleep(random.uniform(0.1, 0.2))
                    
                    # Occasional pause (thinking - 6% chance)
                    if random.random() < 0.06:
                        delay += random.uniform(0.3, 0.8)
                    
                    time.sleep(delay)
                
                # Pause after typing (review)
                time.sleep(random.uniform(0.5, 1.2))
                
                # Click next/submit button
                self.click_next_button()
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"Error entering text: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('survey', 'text_entry_failed', error_msg)
            return False
    
    def select_radio_option(self, answer: str) -> bool:
        """Select radio button option with human-like behavior"""
        try:
            radios = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            
            if radios:
                # Simulate decision making
                self.human_behavior.simulate_decision_making(len(radios))
                
                # Try to match answer text
                selected = False
                for radio in radios:
                    try:
                        label = radio.find_element(By.XPATH, "./following-sibling::label | ./parent::label")
                        
                        # Scroll to option (humans scan options)
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            radio
                        )
                        time.sleep(random.uniform(0.2, 0.4))
                        
                        if answer.lower() in label.text.lower():
                            # Move mouse naturally to option
                            self.human_behavior.natural_mouse_move_to_element(radio)
                            time.sleep(random.uniform(0.2, 0.5))
                            
                            radio.click()
                            selected = True
                            break
                    except:
                        continue
                
                if not selected:
                    # Fallback: select random option (but with human behavior)
                    chosen_radio = random.choice(radios)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        chosen_radio
                    )
                    time.sleep(random.uniform(0.3, 0.6))
                    self.human_behavior.natural_mouse_move_to_element(chosen_radio)
                    time.sleep(random.uniform(0.2, 0.4))
                    chosen_radio.click()
                
                # Pause after selection (humans review their choice)
                time.sleep(random.uniform(0.5, 1.0))
                
                self.click_next_button()
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"Error selecting radio: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('survey', 'radio_selection_failed', error_msg)
            return False
    
    def select_checkbox_option(self, answer: str) -> bool:
        """Select checkbox option"""
        try:
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            
            if checkboxes:
                # Select first checkbox
                checkboxes[0].click()
                self.click_next_button()
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"Error selecting checkbox: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('survey', 'checkbox_selection_failed', error_msg)
            return False
    
    def click_next_button(self):
        """Click next/continue/submit button with human behavior"""
        try:
            # Common button texts
            button_texts = ['Next', 'Continue', 'Submit', 'Weiter', 'Fortfahren', 'Absenden']
            
            button_found = False
            for text in button_texts:
                try:
                    button = self.driver.find_element(By.XPATH, 
                        f"//button[contains(text(), '{text}')] | //input[@value='{text}']")
                    
                    # Scroll to button
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        button
                    )
                    time.sleep(random.uniform(0.3, 0.6))
                    
                    # Move mouse naturally
                    self.human_behavior.natural_mouse_move_to_element(button)
                    
                    # Pause before clicking (humans hesitate slightly)
                    time.sleep(random.uniform(0.3, 0.7))
                    
                    button.click()
                    button_found = True
                    break
                except:
                    continue
            
            if not button_found:
                # Fallback: find any submit button
                buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                    "button[type='submit'], input[type='submit'], button.next, button.continue")
                if buttons:
                    button = buttons[0]
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        button
                    )
                    time.sleep(random.uniform(0.3, 0.6))
                    self.human_behavior.natural_mouse_move_to_element(button)
                    time.sleep(random.uniform(0.3, 0.7))
                    button.click()
                    
        except Exception as e:
            logger.warning(f"Could not find next button: {e}")
    
    def is_survey_complete(self) -> bool:
        """Check if survey is complete"""
        try:
            # Check for completion messages
            completion_texts = ['thank you', 'complete', 'finished', 'danke', 'abgeschlossen']
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            
            return any(text in page_text for text in completion_texts)
            
        except:
            return False
    
    def check_for_errors(self) -> bool:
        """Check for error messages"""
        try:
            error_texts = ['error', 'invalid', 'required', 'fehler', 'ungültig']
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            
            return any(text in page_text for text in error_texts)
            
        except:
            return False
    
    def take_screenshot(self, name: str) -> Path:
        """Take screenshot"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = self.settings.screenshots_dir / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            return filepath
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return None
    
    def save_survey_result(self, survey_url: str, success: bool, questions_answered: int):
        """Save survey result"""
        try:
            import json
            from datetime import datetime
            
            result = {
                'url': survey_url,
                'success': success,
                'questions_answered': questions_answered,
                'timestamp': datetime.now().isoformat()
            }
            
            result_file = self.settings.surveys_dir / f"survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving survey result: {e}")
