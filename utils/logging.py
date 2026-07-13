import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(app):
    """Setup application logging."""
    
    if not app.debug:
        # Create logs directory
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # File handler
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'scriptflow.log'),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('ScriptFlow startup')


def log_error(error, context=None):
    """Log an error with context."""
    logger = logging.getLogger(__name__)
    
    error_info = {
        'type': type(error).__name__,
        'message': str(error),
        'context': context or {}
    }
    
    logger.error(f"Error: {error_info}")


def log_user_action(user_id, action, details=None):
    """Log user actions for analytics."""
    logger = logging.getLogger(__name__)
    
    log_entry = {
        'user_id': user_id,
        'action': action,
        'details': details or {},
        'timestamp': datetime.utcnow().isoformat()
    }
    
    logger.info(f"User Action: {log_entry}")


def log_security_event(event_type, details):
    """Log security-related events."""
    logger = logging.getLogger(__name__)
    
    log_entry = {
        'event_type': event_type,
        'details': details,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    logger.warning(f"Security Event: {log_entry}")
