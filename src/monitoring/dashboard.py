"""Real-time monitoring dashboard"""

import hmac
import json
import traceback
import functools
import psutil
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request, Response
from flask_socketio import SocketIO
from loguru import logger

class MonitoringDashboard:
    """Web-based monitoring dashboard"""
    
    def __init__(self, settings):
        self.settings = settings
        try:
            self.app = Flask(__name__, template_folder=str(settings.base_dir / 'templates'))
            self.app.config['SECRET_KEY'] = settings.effective_secret_key
            self.socketio = SocketIO(self.app, cors_allowed_origins='*')
            
            self.setup_routes()
        except Exception as e:
            logger.error(f"Failed to initialize dashboard: {e}")
            raise

    def _check_auth(self, username: str, password: str) -> bool:
        """Validate dashboard credentials if auth is configured"""
        cfg_user = self.settings.dashboard_username
        cfg_pass = self.settings.dashboard_password
        if not cfg_user or not cfg_pass:
            return True  # Auth not configured, allow all
        return (
            hmac.compare_digest(username, cfg_user)
            and hmac.compare_digest(password, cfg_pass)
        )

    def _auth_required(self, f):
        """Decorator that enforces HTTP Basic Auth when credentials are set"""
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            cfg_user = self.settings.dashboard_username
            cfg_pass = self.settings.dashboard_password
            if cfg_user and cfg_pass:
                auth = request.authorization
                if not auth or not self._check_auth(auth.username, auth.password):
                    return Response(
                        'Authentication required',
                        401,
                        {'WWW-Authenticate': 'Basic realm="Survey Dashboard"'}
                    )
            return f(*args, **kwargs)
        return decorated
    
    def setup_routes(self):
        """Setup Flask routes"""
        auth = self._auth_required
        
        @self.app.route('/')
        @auth
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/stats')
        @auth
        def get_stats():
            try:
                return jsonify(self.get_current_stats())
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/logs')
        @auth
        def get_logs():
            try:
                return jsonify(self.get_recent_logs())
            except Exception as e:
                logger.error(f"Error getting logs: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/system')
        @auth
        def get_system():
            try:
                return jsonify(self.get_system_info())
            except Exception as e:
                logger.error(f"Error getting system info: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/errors')
        @auth
        def get_errors():
            """Get error report from error tracker"""
            try:
                return jsonify(self.get_error_report())
            except Exception as e:
                logger.error(f"Error getting error report: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/health')
        @auth
        def get_health():
            """Get health check status"""
            try:
                return jsonify(self.get_health_status())
            except Exception as e:
                logger.error(f"Error getting health status: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/metrics')
        @auth
        def get_metrics():
            """Get Prometheus metrics"""
            try:
                return self.get_prometheus_metrics(), 200, {'Content-Type': 'text/plain'}
            except Exception as e:
                logger.error(f"Error getting metrics: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/earnings')
        @auth
        def get_earnings():
            """Get earnings report"""
            try:
                return jsonify(self.get_earnings_report())
            except Exception as e:
                logger.error(f"Error getting earnings: {e}")
                return jsonify({'error': str(e)}), 500
    
    def get_current_stats(self) -> dict:
        """Get current automation statistics"""
        try:
            stats_file = self.settings.data_dir / 'stats.json'
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    return json.load(f)
            return {
                'surveys_completed': 0,
                'surveys_failed': 0,
                'captchas_solved': 0
            }
        except Exception as e:
            logger.error(f"Error reading stats: {e}")
            return {}
    
    def get_recent_logs(self, lines: int = 50) -> list:
        """Get recent log entries"""
        try:
            log_file = self.settings.logs_dir / 'automation.log'
            if log_file.exists():
                with open(log_file, 'r') as f:
                    all_lines = f.readlines()
                    return all_lines[-lines:]
            return []
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
            return []
    
    def get_system_info(self) -> dict:
        """Get system resource information"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    def get_error_report(self) -> dict:
        """Get error report from error tracker"""
        try:
            error_file = self.settings.data_dir / 'errors.json'
            if error_file.exists():
                with open(error_file, 'r') as f:
                    return json.load(f)
            return {
                'total_errors': 0,
                'errors_by_category': {},
                'recent_errors': []
            }
        except Exception as e:
            logger.error(f"Error reading error report: {e}")
            return {'error': str(e)}
    
    def get_health_status(self) -> dict:
        """Get health check status"""
        try:
            health_file = self.settings.data_dir / 'health.json'
            if health_file.exists():
                with open(health_file, 'r') as f:
                    return json.load(f)
            return {
                'status': 'unknown',
                'checks': {}
            }
        except Exception as e:
            logger.error(f"Error reading health status: {e}")
            return {'error': str(e)}
    
    def get_prometheus_metrics(self) -> str:
        """Get metrics in Prometheus format"""
        try:
            stats = self.get_current_stats()
            system = self.get_system_info()
            
            metrics = []
            
            # Survey metrics
            metrics.append(f'# HELP surveys_completed_total Total surveys completed')
            metrics.append(f'# TYPE surveys_completed_total counter')
            metrics.append(f'surveys_completed_total {stats.get("surveys_completed", 0)}')
            
            metrics.append(f'# HELP surveys_failed_total Total surveys failed')
            metrics.append(f'# TYPE surveys_failed_total counter')
            metrics.append(f'surveys_failed_total {stats.get("surveys_failed", 0)}')
            
            metrics.append(f'# HELP captchas_solved_total Total CAPTCHAs solved')
            metrics.append(f'# TYPE captchas_solved_total counter')
            metrics.append(f'captchas_solved_total {stats.get("captchas_solved", 0)}')
            
            # System metrics
            metrics.append(f'# HELP system_cpu_percent CPU usage percentage')
            metrics.append(f'# TYPE system_cpu_percent gauge')
            metrics.append(f'system_cpu_percent {system.get("cpu_percent", 0)}')
            
            metrics.append(f'# HELP system_memory_percent Memory usage percentage')
            metrics.append(f'# TYPE system_memory_percent gauge')
            metrics.append(f'system_memory_percent {system.get("memory_percent", 0)}')
            
            metrics.append(f'# HELP system_disk_percent Disk usage percentage')
            metrics.append(f'# TYPE system_disk_percent gauge')
            metrics.append(f'system_disk_percent {system.get("disk_percent", 0)}')
            
            # Success rate
            total = stats.get("surveys_completed", 0) + stats.get("surveys_failed", 0)
            success_rate = (stats.get("surveys_completed", 0) / total * 100) if total > 0 else 0
            metrics.append(f'# HELP success_rate_percent Survey success rate')
            metrics.append(f'# TYPE success_rate_percent gauge')
            metrics.append(f'success_rate_percent {success_rate:.2f}')
            
            return '\n'.join(metrics)
            
        except Exception as e:
            logger.error(f"Error generating metrics: {e}")
            return f'# Error: {e}'
    
    def get_earnings_report(self) -> dict:
        """Get earnings report from earnings file"""
        try:
            earnings_file = self.settings.data_dir / 'earnings.json'
            if earnings_file.exists():
                with open(earnings_file, 'r') as f:
                    return json.load(f)
            return {
                'total_earnings': 0,
                'surveys_completed': 0,
                'average_per_survey': 0,
                'today_earnings': 0,
                'this_week_earnings': 0,
                'this_month_earnings': 0,
                'last_updated': None
            }
        except Exception as e:
            logger.error(f"Error reading earnings: {e}")
            return {'error': str(e)}

    def run(self):
        """Run the dashboard server"""
        try:
            logger.info(f"🌐 Starting dashboard on http://0.0.0.0:{self.settings.flask_port}")
            logger.info(f"📊 Access dashboard at: http://localhost:{self.settings.flask_port}")
            if self.settings.dashboard_username:
                logger.info("🔐 Dashboard authentication enabled")
            self.socketio.run(
                self.app,
                host='0.0.0.0',
                port=self.settings.flask_port,
                debug=self.settings.flask_debug,
                use_reloader=False,
                allow_unsafe_werkzeug=True
            )
        except OSError as e:
            if 'Address already in use' in str(e):
                logger.error(f"❌ Port {self.settings.flask_port} is already in use!")
                logger.error(f"💡 Fix: Stop the other process or change FLASK_PORT in .env")
            else:
                logger.error(f"❌ Dashboard startup error: {e}")
        except Exception as e:
            logger.error(f"❌ Dashboard error: {e}\n{traceback.format_exc()}")
