"""Ollama AI client for vision and decision making"""

import base64
import requests
import json
import traceback
from pathlib import Path
from loguru import logger

class OllamaClient:
    """Client for Ollama AI with vision capabilities"""
    
    def __init__(self, settings, error_tracker=None):
        self.settings = settings
        self.error_tracker = error_tracker
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.persona = settings.persona_dict
    
    def analyze_screenshot(self, image_path: Path, prompt: str) -> dict:
        """Analyze screenshot and return AI decision"""
        try:
            if not image_path or not image_path.exists():
                error_msg = f"Image file not found: {image_path}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'image_not_found', error_msg)
                return {'success': False, 'error': 'Image file not found'}
            
            if not prompt:
                error_msg = "Empty prompt provided"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'empty_prompt', error_msg)
                return {'success': False, 'error': 'Empty prompt'}
            
            # Read and encode image
            try:
                with open(image_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                error_msg = f"Failed to read/encode image: {str(e)}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'image_encoding_failed', error_msg)
                return {'success': False, 'error': 'Image encoding failed'}
            
            # Build persona context
            persona_context = f"""
You are {self.persona['name']}, a {self.persona['age']}-year-old German person.
Your details:
- Address: {self.persona['address']}
- Birthday: {self.persona['birthday']}
- Phone: {self.persona['phone']}
- Mother's maiden name: {self.persona['mother_maiden']}

Respond naturally as this person would, in German when appropriate.
"""
            
            # Make API request
            try:
                response = requests.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{persona_context}\n\n{prompt}",
                        "images": [image_data],
                        "stream": False
                    },
                    timeout=60
                )
            except requests.Timeout:
                error_msg = "Ollama API request timed out (60s)"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'api_timeout', error_msg)
                return {'success': False, 'error': 'API timeout'}
            except requests.ConnectionError as e:
                error_msg = f"Cannot connect to Ollama at {self.host}: {str(e)}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'connection_failed', error_msg)
                return {'success': False, 'error': 'Connection failed'}
            except Exception as e:
                error_msg = f"Ollama API request failed: {str(e)}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'api_request_failed', error_msg)
                return {'success': False, 'error': str(e)}
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    ai_response = result.get('response', '')
                    
                    if not ai_response:
                        logger.warning("Ollama returned empty response")
                        if self.error_tracker:
                            self.error_tracker.log_error('ai', 'empty_response', 'Ollama returned empty response')
                    
                    logger.debug(f"AI Response: {ai_response[:200]}...")
                    
                    return {
                        'success': True,
                        'response': ai_response,
                        'raw': result
                    }
                except json.JSONDecodeError as e:
                    error_msg = f"Failed to parse Ollama response: {str(e)}"
                    logger.error(error_msg)
                    if self.error_tracker:
                        self.error_tracker.log_error('ai', 'response_parse_failed', error_msg)
                    return {'success': False, 'error': 'Response parse failed'}
            else:
                error_msg = f"Ollama API error: {response.status_code} - {response.text[:200]}"
                logger.error(error_msg)
                if self.error_tracker:
                    self.error_tracker.log_error('ai', 'api_error', error_msg)
                return {'success': False, 'error': f"API error: {response.status_code}"}
                
        except Exception as e:
            error_msg = f"Error analyzing screenshot: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('ai', 'analysis_failed', error_msg)
            return {'success': False, 'error': str(e)}
    
    def extract_button_coordinates(self, image_path: Path) -> dict:
        """Extract button coordinates from screenshot"""
        prompt = """
Analyze this webpage screenshot and identify the login button.
Provide the approximate X,Y coordinates as percentages of the image dimensions.
Respond in JSON format: {"button_found": true/false, "x_percent": 50, "y_percent": 30, "description": "Login button"}
"""
        result = self.analyze_screenshot(image_path, prompt)
        
        if result['success']:
            try:
                # Try to parse JSON from response
                response_text = result['response']
                # Extract JSON if embedded in text
                if '{' in response_text:
                    json_start = response_text.index('{')
                    json_end = response_text.rindex('}') + 1
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except Exception as e:
                logger.warning(f"Could not parse coordinates: {e}")
        
        return {'button_found': False}
    
    def detect_captcha(self, image_path: Path) -> dict:
        """Detect if CAPTCHA is present"""
        prompt = """
Analyze this screenshot and determine if there is a CAPTCHA or reCAPTCHA present.
Look for:
- reCAPTCHA checkbox ("I'm not a robot")
- Image selection grids
- Text input for CAPTCHA codes
- Any anti-bot verification

Respond in JSON format: {"captcha_present": true/false, "captcha_type": "recaptcha_v2/recaptcha_v3/image/text/none", "description": "..."}
"""
        result = self.analyze_screenshot(image_path, prompt)
        
        if result['success']:
            try:
                response_text = result['response']
                if '{' in response_text:
                    json_start = response_text.index('{')
                    json_end = response_text.rindex('}') + 1
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except Exception as e:
                logger.warning(f"Could not parse CAPTCHA detection: {e}")
        
        return {'captcha_present': False, 'captcha_type': 'none'}
    
    def answer_survey_question(self, image_path: Path, question_text: str = None) -> dict:
        """Generate answer for survey question"""
        prompt = f"""
Analyze this survey question and provide an appropriate answer as {self.persona['name']}.

Question text (if available): {question_text or 'See image'}

Consider:
- Your age ({self.persona['age']}) and background
- German cultural context
- Realistic and consistent responses
- Detect trap questions (e.g., "Are you on the moon?") and answer correctly

Respond in JSON format: {{"answer_type": "text/radio/checkbox", "answer": "your answer", "reasoning": "why this answer"}}
"""
        result = self.analyze_screenshot(image_path, prompt)
        
        if result['success']:
            try:
                response_text = result['response']
                if '{' in response_text:
                    json_start = response_text.index('{')
                    json_end = response_text.rindex('}') + 1
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except Exception as e:
                logger.warning(f"Could not parse answer: {e}")
                # Return text response as fallback
                return {
                    'answer_type': 'text',
                    'answer': result['response'][:200],
                    'reasoning': 'AI generated response'
                }
        
        return {'answer_type': 'text', 'answer': '', 'reasoning': 'Failed to generate'}
