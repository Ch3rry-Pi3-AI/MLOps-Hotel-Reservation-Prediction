"""
logger.py
----------------
Centralised logging configuration module for the MLOps project.

This script sets up a standardised logging system that writes log files
to a dedicated `logs/` directory, automatically creating a new log file
for each day based on the current date.

It provides a simple helper function, `get_logger(name)`, that returns
a configured logger instance for use across modules.

Usage
-----
Example (within any module):

    from src.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Model training started.")
    logger.error("Failed to connect to database.")

Notes
-----
- All logs are written to `logs/log_YYYY-MM-DD.log`
- Each message is timestamped and tagged with severity.
- Default level: INFO
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import logging
import os
from datetime import datetime

# -------------------------------------------------------------------
# Directory Setup
# -------------------------------------------------------------------
# Ensure the 'logs' directory exists
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Log File Configuration
# -------------------------------------------------------------------
# Create a log file named with the current date
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging format and severity level
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -------------------------------------------------------------------
# Logger Factory Function
# -------------------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance with the specified name.

    Parameters
    ----------
    name : str
        The name of the logger, typically set to `__name__`.

    Returns
    -------
    logging.Logger
        A logger object with INFO-level configuration.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger