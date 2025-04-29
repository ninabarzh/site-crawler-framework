"""
Configuration loading and validation.
"""

import yaml
from pathlib import Path
from typing import Dict, Any

from src.core import ConfigError


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration

    Raises:
        ConfigError: If the file cannot be loaded or parsed
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
        return validate_config(config)
    except yaml.YAMLError as e:
        raise ConfigError(f"YAML parsing error: {str(e)}")
    except IOError as e:
        raise ConfigError(f"Configuration file error: {str(e)}")


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and set default values for configuration.

    Args:
        config: Configuration dictionary to validate

    Returns:
        Validated configuration dictionary

    Raises:
        ConfigError: If required configuration is missing
    """
    # Set defaults for required values
    defaults = {
        'crawler': {
            'max_depth': 3,
            'request_timeout': 10,
            'user_agent': 'SiteCrawler/1.0',
            'concurrent_requests': 5,
            'retry_attempts': 3,
            'politeness_delay': 1.0
        },
        'storage': {
            'output_dir': './output',
            'save_html': True,
            'save_pdf': True,
            'save_images': False
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'crawler.log'
        }
    }

    # Merge defaults with provided config
    for section, section_defaults in defaults.items():
        if section not in config:
            config[section] = section_defaults
        else:
            for key, value in section_defaults.items():
                if key not in config[section]:
                    config[section][key] = value

    # Ensure output directory exists
    output_dir = Path(config['storage']['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)

    return config
