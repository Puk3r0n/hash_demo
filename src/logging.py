"""
Module responsible for setting up logging using Loguru.
"""

from loguru import logger

logger.add("file_{time}.log", rotation="1 day")
