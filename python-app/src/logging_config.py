import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir='logs'):
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger('crud_app')
    logger.setLevel(logging.DEBUG)

    # Create file handler that overwrites the file
    log_file = os.path.join(log_dir, 'crud_app.log')
    file_handler = logging.FileHandler(
        log_file,
        mode='w'  # 'w' mode overwrites the file
    )
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger