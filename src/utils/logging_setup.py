import logging
import os
import sys
from pathlib import Path

def setup_logging(name: str = "supportpearlz") -> logging.Logger:
    """Configures centralized logging for the application."""
    logger = logging.getLogger(name)
    
    # Avoid adding duplicate handlers if already configured
    if logger.handlers:
        return logger

    # Get log level safely from environment or default to INFO
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (optional for local/cloud)
    try:
        log_dir = Path("data")
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler("supportpearlz.log", encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    except Exception:
        pass  # Skip file logging if filesystem is read-only (like Streamlit Cloud)

    return logger