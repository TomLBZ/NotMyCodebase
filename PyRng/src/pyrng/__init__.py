"""PyRng - Python Random Number Generator.

A highly configurable command-line random number generator with support
for multiple probability distributions and output formats.

Version: 1.0.0
Author: PyRng Development Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "PyRng Development Team"
__license__ = "MIT"

from pyrng.core.generator import RandomGenerator
from pyrng.core.exceptions import (
    PyRngError,
    ValidationError,
    DistributionError,
    OutputError,
    ConfigurationError,
)

__all__ = [
    "RandomGenerator",
    "PyRngError",
    "ValidationError",
    "DistributionError",
    "OutputError",
    "ConfigurationError",
]
