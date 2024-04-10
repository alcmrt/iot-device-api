"""
Logging configuration
"""

from logging.config import dictConfig
from iot_device_api.config import config, DevConfig


def configure_logging():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s"
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console"
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "iot_device_api.log",
                    "maxBytes": 1024 * 1024, # 1MB
                    "backupCount": 5,
                    "encoding": "utf8"
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "iot_device_api": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"}
            }
        }
    )