"""
Module responsible for setting up logging using Loguru.
"""

import os
from loguru import logger

log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
logger.add(f"{log_dir}/file_{{time}}.log", rotation="1 day")
