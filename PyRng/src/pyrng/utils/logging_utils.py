"""Logging utilities for PyRng."""

import logging
import sys
from typing import Optional


def setup_logging(
    verbose: bool = False,
    log_file: Optional[str] = None,
    level: Optional[int] = None
) -> None:
    """Configure logging for PyRng application.
    
    This function sets up the logging system with appropriate handlers,
    formatters, and log levels based on the provided configuration.
    
    Args:
        verbose: Enable verbose logging (DEBUG level). If False, uses INFO level.
        log_file: Optional path to log file. If provided, logs to both file and console.
        level: Explicit log level override. If provided, takes precedence over verbose.
    
    Examples:
        >>> # Basic setup with INFO level
        >>> setup_logging()
        
        >>> # Verbose logging to console
        >>> setup_logging(verbose=True)
        
        >>> # Log to file and console
        >>> setup_logging(verbose=True, log_file="pyrng.log")
    """
    # Determine log level
    if level is not None:
        log_level = level
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    # Create formatter
    if verbose:
        fmt = "[%(asctime)s] %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
    else:
        fmt = "%(levelname)-8s: %(message)s"
    
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Log initial message
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured: level={logging.getLevelName(log_level)}")
    if log_file:
        logger.debug(f"Logging to file: {log_file}")
