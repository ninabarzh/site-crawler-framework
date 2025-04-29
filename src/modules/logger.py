"""
Logging configuration and utilities.
"""

import logging
import logging.config
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]):
    """
    Configure logging based on the provided configuration.

    Args:
        config: Dictionary containing logging configuration
    """
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': config.get('level', 'INFO')
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': config.get('level', 'INFO'),
                'propagate': True
            }
        }
    }

    # Add file handler if configured
    if config.get('file'):
        log_config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'filename': config['file'],
            'formatter': 'standard',
            'level': config.get('level', 'INFO')
        }
        log_config['loggers']['']['handlers'].append('file')

    logging.config.dictConfig(log_config)


def get_logger(name: str, config: Dict[str, Any]) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name
        config: Logging configuration

    Returns:
        Configured logger instance
    """
    setup_logging(config)
    return logging.getLogger(name)
