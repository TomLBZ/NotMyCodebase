"""Output writing utilities."""

import sys
from pathlib import Path
from typing import Union, Optional
import logging

import numpy as np

from pyrng.output.formatters import (
    TextFormatter,
    CSVFormatter,
    JSONFormatter,
    BinaryFormatter,
)
from pyrng.output.base import OutputFormatter
from pyrng.core.exceptions import OutputError

logger = logging.getLogger(__name__)


class OutputWriter:
    """Handles writing formatted output to files or stdout.
    
    Examples:
        >>> writer = OutputWriter(formatter=TextFormatter())
        >>> data = np.array([1, 2, 3])
        >>> writer.write_to_stdout(data)
        1
        2
        3
    """
    
    def __init__(self, formatter: OutputFormatter) -> None:
        """Initialize output writer.
        
        Args:
            formatter: OutputFormatter instance for formatting data.
        """
        self.formatter = formatter
    
    def write_to_stdout(self, data: np.ndarray) -> None:
        """Write formatted data to stdout.
        
        Args:
            data: NumPy array of samples to write.
        """
        formatted = self.formatter.format(data)
        
        # Binary data needs special handling
        if isinstance(formatted, bytes):
            sys.stdout.buffer.write(formatted)
        else:
            print(formatted)
    
    def write_to_file(self, data: np.ndarray, file_path: Union[str, Path]) -> None:
        """Write formatted data to a file.
        
        Args:
            data: NumPy array of samples to write.
            file_path: Path to output file.
        
        Raises:
            OutputError: If file writing fails.
        """
        path = Path(file_path)
        
        try:
            # Create parent directories if they don't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            formatted = self.formatter.format(data)
            
            # Write binary or text data
            if isinstance(formatted, bytes):
                path.write_bytes(formatted)
                logger.info(f"Wrote {len(formatted)} bytes to {path}")
            else:
                path.write_text(formatted, encoding="utf-8")
                logger.info(f"Wrote data to {path}")
                
        except Exception as e:
            raise OutputError(f"Failed to write to {path}: {e}") from e


def get_formatter(
    format_type: str,
    **kwargs: Union[str, bool]
) -> OutputFormatter:
    """Get an output formatter by type.
    
    Args:
        format_type: Format type ("text", "csv", "json", or "binary").
        **kwargs: Format-specific options.
    
    Returns:
        OutputFormatter instance.
    
    Raises:
        OutputError: If format type is unknown.
    
    Examples:
        >>> fmt = get_formatter("text")
        >>> isinstance(fmt, TextFormatter)
        True
        
        >>> fmt = get_formatter("csv", header="values")
        >>> isinstance(fmt, CSVFormatter)
        True
    """
    format_lower = format_type.lower()
    
    formatters = {
        "text": TextFormatter,
        "csv": CSVFormatter,
        "json": JSONFormatter,
        "binary": BinaryFormatter,
    }
    
    if format_lower not in formatters:
        available = ", ".join(sorted(formatters.keys()))
        raise OutputError(
            f"Unknown format type: '{format_type}'. "
            f"Available formats: {available}"
        )
    
    formatter_class = formatters[format_lower]
    
    try:
        return formatter_class(**kwargs)
    except TypeError as e:
        raise OutputError(
            f"Invalid options for {format_type} formatter: {e}"
        ) from e


def write_output(
    data: np.ndarray,
    output_path: Optional[Union[str, Path]],
    format_type: str = "text",
    **format_options: Union[str, bool]
) -> None:
    """Write data to file or stdout with specified format.
    
    Convenience function that combines formatter creation and output writing.
    
    Args:
        data: NumPy array of samples to write.
        output_path: Path to output file. If None, writes to stdout.
        format_type: Output format ("text", "csv", "json", or "binary").
        **format_options: Format-specific options.
    
    Examples:
        >>> data = np.array([1, 2, 3])
        >>> write_output(data, None, "text")  # To stdout
        >>> write_output(data, "output.csv", "csv", header="values")
        >>> write_output(data, "output.json", "json", pretty=True)
    """
    formatter = get_formatter(format_type, **format_options)
    writer = OutputWriter(formatter)
    
    if output_path is None:
        writer.write_to_stdout(data)
    else:
        writer.write_to_file(data, output_path)
