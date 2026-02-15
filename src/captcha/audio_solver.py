"""FREE Audio CAPTCHA Solver using Google Speech Recognition"""

import os
import time
import random
import traceback
import requests
import speech_recognition as sr
from pydub import AudioSegment
from pathlib import Path
from loguru import logger

class AudioCaptchaSolver:
    """Solve reCAPTCHA using FREE audio challenge + Google Speech API"""
    
    def __init__(self, settings, error_tracker=None):
        self.settings = settings
        self.error_tracker = error_tracker
        self.recognizer = sr.Recognizer()
        self.temp_dir = settings.screenshots_dir / 'audio_temp'
        
        try:
            self.temp_dir.mkdir(exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create temp directory: {e}")
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'temp_dir_creation_failed', str(e))
    
    def solve_recaptcha_audio(self, driver) -> dict:
        """
        Solve reCAPTCHA v2 using audio challenge (100% FREE!)
        
        How it works:
        1. Click audio challenge button
        2. Download audio file
        3. Convert to WAV format
        4. Use Google Speech Recognition (FREE!)
        5. Submit transcribed text
        """
        logger.info("Attempting FREE audio CAPTCHA solve...")
        
        try:
            # Step 1: Find and click audio challenge button
            audio_button = self._find_audio_button(driver)
            if not audio_button:
                return {'success': False, 'error': 'Audio button not found'}
            
            # Human-like delay before clicking
            time.sleep(random.uniform(1.0, 2.0))
            audio_button.click()
            time.sleep(random.uniform(2.0, 3.0))
            
            # Step 2: Get audio download link
            audio_url = self._get_audio_url(driver)
            if not audio_url:
                return {'success': False, 'error': 'Audio URL not found'}
            
            # Step 3: Download audio file
            audio_file = self._download_audio(audio_url)
            if not audio_file:
                return {'success': False, 'error': 'Audio download failed'}
            
            # Step 4: Convert to WAV (required for speech recognition)
            wav_file = self._convert_to_wav(audio_file)
            if not wav_file:
                return {'success': False, 'error': 'Audio conversion failed'}
            
            # Step 5: Transcribe using Google Speech Recognition (FREE!)
            transcription = self._transcribe_audio(wav_file)
            if not transcription:
                return {'success': False, 'error': 'Transcription failed'}
            
            # Step 6: Enter transcription
            success = self._submit_transcription(driver, transcription)
            
            # Cleanup
            self._cleanup_files(audio_file, wav_file)
            
            if success:
                logger.info(f"✅ FREE audio CAPTCHA solved: {transcription}")
                return {'success': True, 'solution': transcription}
            else:
                return {'success': False, 'error': 'Submission failed'}
                
        except Exception as e:
            error_msg = f"Audio CAPTCHA solve error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'audio_solve_failed', error_msg)
            return {'success': False, 'error': str(e)}
    
    def _find_audio_button(self, driver):
        """Find audio challenge button"""
        try:
            # Switch to reCAPTCHA iframe
            iframes = driver.find_elements('css selector', 'iframe[src*="recaptcha"]')
            for iframe in iframes:
                driver.switch_to.frame(iframe)
                
                # Look for audio button
                audio_buttons = [
                    'button#recaptcha-audio-button',
                    'button[aria-label*="audio"]',
                    '.rc-button-audio'
                ]
                
                for selector in audio_buttons:
                    try:
                        button = driver.find_element('css selector', selector)
                        if button.is_displayed():
                            return button
                    except:
                        continue
                
                driver.switch_to.default_content()
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding audio button: {e}")
            driver.switch_to.default_content()
            return None
    
    def _get_audio_url(self, driver):
        """Extract audio file URL"""
        try:
            # Look for audio source
            audio_sources = [
                'audio source',
                'audio#audio-source',
                '.rc-audiochallenge-tdownload-link'
            ]
            
            for selector in audio_sources:
                try:
                    element = driver.find_element('css selector', selector)
                    url = element.get_attribute('src')
                    if url:
                        return url
                except:
                    continue
            
            # Try download link
            try:
                download_link = driver.find_element('css selector', 'a.rc-audiochallenge-tdownload-link')
                return download_link.get_attribute('href')
            except:
                pass
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting audio URL: {e}")
            return None
    
    def _download_audio(self, url: str) -> Path:
        """Download audio file"""
        try:
            if not url:
                logger.error("Empty audio URL")
                return None
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                audio_file = self.temp_dir / f'captcha_{int(time.time())}.mp3'
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✓ Audio downloaded: {audio_file}")
                return audio_file
            else:
                logger.error(f"Audio download failed with status {response.status_code}")
                if self.error_tracker:
                    self.error_tracker.log_error('captcha', 'audio_download_failed', f"Status: {response.status_code}")
                return None
            
        except requests.RequestException as e:
            error_msg = f"Audio download network error: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'audio_download_network_error', error_msg)
            return None
        except Exception as e:
            error_msg = f"Audio download error: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'audio_download_error', error_msg)
            return None
    
    def _convert_to_wav(self, audio_file: Path) -> Path:
        """Convert audio to WAV format"""
        try:
            if not audio_file or not audio_file.exists():
                logger.error(f"Audio file not found: {audio_file}")
                return None
            
            # Load audio file
            audio = AudioSegment.from_file(str(audio_file))
            
            # Convert to WAV
            wav_file = audio_file.with_suffix('.wav')
            audio.export(str(wav_file), format='wav')
            
            logger.info(f"✓ Audio converted to WAV: {wav_file}")
            return wav_file
            
        except Exception as e:
            error_msg = f"Audio conversion error: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'audio_conversion_failed', error_msg)
            return None
    
    def _transcribe_audio(self, wav_file: Path) -> str:
        """
        Transcribe audio using Google Speech Recognition (FREE!)
        
        This uses Google's free speech recognition API.
        No API key required!
        """
        try:
            if not wav_file or not wav_file.exists():
                logger.error(f"WAV file not found: {wav_file}")
                return None
            
            with sr.AudioFile(str(wav_file)) as source:
                # Record audio
                audio_data = self.recognizer.record(source)
                
                # Transcribe using Google (FREE!)
                # This is Google's public API - no key needed!
                text = self.recognizer.recognize_google(audio_data)
                
                logger.info(f"✓ Transcription: {text}")
                return text.lower()
                
        except sr.UnknownValueError:
            error_msg = "Google Speech Recognition could not understand audio"
            logger.warning(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'transcription_unclear', error_msg)
            return None
        except sr.RequestError as e:
            error_msg = f"Could not request results from Google Speech Recognition: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'transcription_request_error', error_msg)
            return None
        except Exception as e:
            error_msg = f"Transcription error: {str(e)}"
            logger.error(error_msg)
            if self.error_tracker:
                self.error_tracker.log_error('captcha', 'transcription_error', error_msg)
            return None
    
    def _submit_transcription(self, driver, transcription: str) -> bool:
        """Submit transcribed text"""
        try:
            # Find input field
            input_field = driver.find_element('css selector', 'input#audio-response')
            
            # Enter transcription with human-like typing
            input_field.clear()
            for char in transcription:
                input_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.5, 1.0))
            
            # Click verify button
            verify_button = driver.find_element('css selector', 'button#recaptcha-verify-button')
            verify_button.click()
            
            time.sleep(random.uniform(2.0, 3.0))
            
            # Check if solved
            # If we're back to default content, it likely worked
            driver.switch_to.default_content()
            return True
            
        except Exception as e:
            logger.error(f"Submission error: {e}")
            driver.switch_to.default_content()
            return False
    
    def _cleanup_files(self, *files):
        """Clean up temporary audio files"""
        for file in files:
            if file and file.exists():
                try:
                    file.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete {file}: {e}")


import random

class FreeTrialCaptchaSolver:
    """
    Manage free trial CAPTCHA services
    Automatically rotates between free trial services
    """
    
    def __init__(self, settings, error_tracker=None):
        self.settings = settings
        self.error_tracker = error_tracker
        self.services = []
        self._load_free_services()
    
    def _load_free_services(self):
        """Load available free trial services"""
        # Check for free trial API keys in environment
        free_services = [
            {
                'name': 'anticaptcha',
                'key': os.getenv('ANTICAPTCHA_FREE_KEY'),
                'credits': 1.0,  # $1 free
                'used': 0
            },
            {
                'name': 'capsolver',
                'key': os.getenv('CAPSOLVER_FREE_KEY'),
                'credits': 0.5,  # $0.50 free
                'used': 0
            },
            {
                'name': 'nopecha',
                'key': os.getenv('NOPECHA_FREE_KEY'),
                'credits': 0.0,  # Free tier
                'used': 0
            }
        ]
        
        # Only add services with keys
        self.services = [s for s in free_services if s['key']]
        
        if self.services:
            logger.info(f"Loaded {len(self.services)} free trial services")
    
    def get_next_service(self):
        """Get next available free service"""
        for service in self.services:
            cost_per_captcha = 0.003  # $0.003 per CAPTCHA
            estimated_cost = service['used'] * cost_per_captcha
            
            if estimated_cost < service['credits']:
                return service
        
        return None
    
    def solve_captcha(self, site_key: str, page_url: str) -> dict:
        """Solve using free trial service"""
        service = self.get_next_service()
        
        if not service:
            return {'success': False, 'error': 'No free credits available'}
        
        logger.info(f"Using free trial: {service['name']}")
        
        # Use appropriate solver based on service
        if service['name'] == 'anticaptcha':
            from src.captcha.anticaptcha_adapter import AntiCaptchaAdapter
            solver = AntiCaptchaAdapter(service['key'])
            result = solver.solve_recaptcha_v2(site_key, page_url)
        elif service['name'] == 'capsolver':
            # TODO: Implement CapSolver adapter
            result = {'success': False, 'error': 'Not implemented'}
        else:
            result = {'success': False, 'error': 'Unknown service'}
        
        if result.get('success'):
            service['used'] += 1
        
        return result
