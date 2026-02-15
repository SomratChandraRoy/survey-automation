"""Stealth browser configuration with advanced anti-detection"""

import random
from loguru import logger

class StealthBrowser:
    """Apply advanced stealth techniques to avoid detection"""
    
    def __init__(self, settings):
        self.settings = settings
    
    def apply_stealth(self, driver):
        """Apply all stealth techniques"""
        logger.info("Applying advanced stealth configurations...")
        
        # Remove webdriver property
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
        
        # Override automation indicators
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Remove automation flags
                delete navigator.__proto__.webdriver;
                
                // Override chrome property
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
            '''
        })
        
        # Override permissions
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            '''
        })
        
        # Override plugins with realistic values
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        },
                        {
                            0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable"},
                            1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable"},
                            description: "",
                            filename: "internal-nacl-plugin",
                            length: 2,
                            name: "Native Client"
                        }
                    ]
                });
            '''
        })
        
        # Override languages
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['de-DE', 'de', 'en-US', 'en']
                });
            '''
        })
        
        # Override platform
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'Win32'
                });
            '''
        })
        
        # Override hardware concurrency (realistic CPU cores)
        cores = random.choice([4, 6, 8, 12, 16])
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                Object.defineProperty(navigator, 'hardwareConcurrency', {{
                    get: () => {cores}
                }});
            '''
        })
        
        # Override device memory (realistic RAM)
        memory = random.choice([4, 8, 16, 32])
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                Object.defineProperty(navigator, 'deviceMemory', {{
                    get: () => {memory}
                }});
            '''
        })
        
        # Override screen resolution (common resolutions)
        resolutions = [
            (1920, 1080),
            (1366, 768),
            (1440, 900),
            (1536, 864),
            (1600, 900)
        ]
        width, height = random.choice(resolutions)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                Object.defineProperty(screen, 'width', {{
                    get: () => {width}
                }});
                Object.defineProperty(screen, 'height', {{
                    get: () => {height}
                }});
                Object.defineProperty(screen, 'availWidth', {{
                    get: () => {width}
                }});
                Object.defineProperty(screen, 'availHeight', {{
                    get: () => {height - 40}
                }});
            '''
        })
        
        # Disable WebRTC
        driver.execute_cdp_cmd('Network.enable', {})
        driver.execute_cdp_cmd('Network.setBlockedURLs', {
            'urls': ['*webrtc*', '*stun*', '*turn*']
        })
        
        # Override WebRTC
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Disable WebRTC
                if (typeof RTCPeerConnection !== 'undefined') {
                    RTCPeerConnection.prototype.createDataChannel = function() {
                        return null;
                    };
                }
            '''
        })
        
        # Set geolocation
        driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
            'latitude': self.settings.persona_geo_lat,
            'longitude': self.settings.persona_geo_lon,
            'accuracy': 100
        })
        
        # Set timezone
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
            'timezoneId': 'Europe/Berlin'
        })
        
        # Set locale
        driver.execute_cdp_cmd('Emulation.setLocaleOverride', {
            'locale': 'de-DE'
        })
        
        # Override canvas fingerprinting
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {
                    // Add slight noise to canvas fingerprint
                    const context = this.getContext('2d');
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                    }
                    context.putImageData(imageData, 0, 0);
                    return originalToDataURL.apply(this, arguments);
                };
            '''
        })
        
        # Override audio context fingerprinting
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                const audioContext = window.AudioContext || window.webkitAudioContext;
                if (audioContext) {
                    const originalCreateOscillator = audioContext.prototype.createOscillator;
                    audioContext.prototype.createOscillator = function() {
                        const oscillator = originalCreateOscillator.apply(this, arguments);
                        const originalStart = oscillator.start;
                        oscillator.start = function() {
                            // Add slight noise
                            this.frequency.value += Math.random() * 0.001;
                            return originalStart.apply(this, arguments);
                        };
                        return oscillator;
                    };
                }
            '''
        })
        
        # Override battery API
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                if (navigator.getBattery) {
                    navigator.getBattery = () => Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 1.0
                    });
                }
            '''
        })
        
        # Override connection API
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        downlink: 10,
                        rtt: 50,
                        saveData: false
                    })
                });
            '''
        })
        
        logger.info("Advanced stealth configurations applied successfully")

