import os
import logging

# Check if running on Vercel production
IS_VERCEL = os.environ.get("VERCEL") == "1"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers to prevent duplicate logs
    logger.handlers = []

    # Always add Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Only create file logs if NOT on Vercel
    if not IS_VERCEL:
        LOG_DIR = "logs"
        os.makedirs(LOG_DIR, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)