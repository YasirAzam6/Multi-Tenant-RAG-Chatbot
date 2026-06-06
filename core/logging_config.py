import logging
import os
from core.config import config

# Only define and create the log directory if we are NOT running on Vercel
IS_VERCEL = os.environ.get("VERCEL") == "1" or os.environ.get("VERCEL") is not None

LOG_DIR = "logs"

if not IS_VERCEL:
    os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    """
    Configures application-wide logging.
    Logs go to both console and a file in the tenant root directory (local only).
    """

    level = logging.DEBUG if config.DEBUG else logging.INFO

    # Always log to the console/stdout (Vercel captures this automatically)
    handlers = [logging.StreamHandler()]

    # Only log to a file if we are running locally
    if not IS_VERCEL:
        handlers.append(logging.FileHandler(os.path.join(LOG_DIR, "app.log")))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )