import logging
from typing import Optional

def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure logging for the application
    
    :param level: Logging level (e.g., 'INFO', 'DEBUG', 'ERROR')
    :return: Configured logger
    """
    numeric_level = getattr(logging, level or 'INFO')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('npo_audit.log')
        ]
    )
    
    return logging.getLogger(__name__)