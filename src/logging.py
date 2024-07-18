from loguru import logger

logger.add("file_{time}.log", rotation="1 day")