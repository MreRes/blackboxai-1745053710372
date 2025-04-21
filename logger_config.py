import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='financial_planner.log'):
    logger = logging.getLogger('financial_planner')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger

logger = setup_logger()
