import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configure logging for the ResumeAI application
    """
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    log_file = os.path.join(log_dir, 'resumeai.log')
    log_level = os.getenv('LOG_LEVEL', 'INFO')

    # Create a custom logger
    logger = logging.getLogger('ResumeAI')
    logger.setLevel(getattr(logging, log_level))

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = setup_logging()
