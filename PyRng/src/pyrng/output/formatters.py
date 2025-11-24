"""Output formatter implementations."""

import numpy as np
import json
import struct
from typing import Any, List

from pyrng.output.base import OutputFormatter
from pyrng.core.exceptions import OutputError


class TextFormatter(OutputFormatter):
    """Plain text output formatter.
    
    Formats data as newline-separated text values.
    
    Attributes:
        delimiter: Delimiter for separating values. Default: "\\n".
    
    Examples:
        >>> formatter = TextFormatter()
        >>> data = np.array([1.5, 2.7, 3.9])
        >>> result = formatter.format(data)
        >>> print(result)
        1.5
        2.7
        3.9
    """
    
    def __init__(self, delimiter: str = "\n") -> None:
        """Initialize text formatter.
        
        Args:
            delimiter: Delimiter for separating values.
        """
        self.delimiter = delimiter
    
    def format(self, data: np.ndarray) -> str:
        """Format data as delimited text.
        
        Args:
            data: NumPy array of samples.
        
        Returns:
            String with delimited values.
        """
        # Convert to Python list for consistent formatting
        values = data.tolist()
        return self.delimiter.join(str(v) for v in values)
    
    def get_extension(self) -> str:
        """Get file extension for text format.
        
        Returns:
            File extension ".txt".
        """
        return ".txt"


class CSVFormatter(OutputFormatter):
    """CSV output formatter.
    
    Formats data as comma-separated values with optional header.
    
    Attributes:
        header: Optional header row. Default: None.
        delimiter: Field delimiter. Default: ",".
    
    Examples:
        >>> formatter = CSVFormatter(header="value")
        >>> data = np.array([1, 2, 3])
        >>> result = formatter.format(data)
        >>> print(result)
        value
        1
        2
        3
    """
    
    def __init__(self, header: str = "value", delimiter: str = ",") -> None:
        """Initialize CSV formatter.
        
        Args:
            header: Column header. If None, no header row.
            delimiter: Field delimiter.
        """
        self.header = header
        self.delimiter = delimiter
    
    def format(self, data: np.ndarray) -> str:
        """Format data as CSV.
        
        Args:
            data: NumPy array of samples.
        
        Returns:
            CSV-formatted string.
        """
        lines: List[str] = []
        
        # Add header if specified
        if self.header:
            lines.append(self.header)
        
        # Add data rows
        values = data.tolist()
        lines.extend(str(v) for v in values)
        
        return "\n".join(lines)
    
    def get_extension(self) -> str:
        """Get file extension for CSV format.
        
        Returns:
            File extension ".csv".
        """
        return ".csv"


class JSONFormatter(OutputFormatter):
    """JSON output formatter.
    
    Formats data as JSON array or object with metadata.
    
    Attributes:
        pretty: Enable pretty printing with indentation. Default: False.
        include_metadata: Include metadata in output. Default: False.
    
    Examples:
        >>> formatter = JSONFormatter(pretty=True)
        >>> data = np.array([1, 2, 3])
        >>> result = formatter.format(data)
        >>> json.loads(result)
        [1, 2, 3]
    """
    
    def __init__(self, pretty: bool = False, include_metadata: bool = False) -> None:
        """Initialize JSON formatter.
        
        Args:
            pretty: Enable pretty printing.
            include_metadata: Include metadata (count, min, max, etc.).
        """
        self.pretty = pretty
        self.include_metadata = include_metadata
    
    def format(self, data: np.ndarray) -> str:
        """Format data as JSON.
        
        Args:
            data: NumPy array of samples.
        
        Returns:
            JSON-formatted string.
        """
        # Convert to Python list for JSON serialization
        values = data.tolist()
        
        if self.include_metadata:
            output = {
                "data": values,
                "metadata": {
                    "count": len(values),
                    "min": float(np.min(data)),
                    "max": float(np.max(data)),
                    "mean": float(np.mean(data)),
                    "std": float(np.std(data)),
                }
            }
        else:
            output = values
        
        indent = 2 if self.pretty else None
        return json.dumps(output, indent=indent)
    
    def get_extension(self) -> str:
        """Get file extension for JSON format.
        
        Returns:
            File extension ".json".
        """
        return ".json"


class BinaryFormatter(OutputFormatter):
    """Binary output formatter.
    
    Formats data as binary packed values.
    
    Attributes:
        dtype: NumPy data type for packing. Default: "float64".
        endian: Byte order ("<" for little, ">" for big). Default: "<".
    
    Examples:
        >>> formatter = BinaryFormatter(dtype="float32")
        >>> data = np.array([1.0, 2.0, 3.0])
        >>> result = formatter.format(data)
        >>> isinstance(result, bytes)
        True
    """
    
    def __init__(self, dtype: str = "float64", endian: str = "<") -> None:
        """Initialize binary formatter.
        
        Args:
            dtype: NumPy data type for binary packing.
            endian: Byte order ("<" for little-endian, ">" for big-endian).
        
        Raises:
            OutputError: If dtype or endian is invalid.
        """
        self.dtype = dtype
        self.endian = endian
        
        # Validate dtype
        try:
            np.dtype(dtype)
        except TypeError as e:
            raise OutputError(f"Invalid dtype '{dtype}': {e}") from e
        
        # Validate endian
        if endian not in ("<", ">", "=", "@", "|"):
            raise OutputError(
                f"Invalid endian '{endian}'. Must be one of: <, >, =, @, |"
            )
    
    def format(self, data: np.ndarray) -> bytes:
        """Format data as binary.
        
        Args:
            data: NumPy array of samples.
        
        Returns:
            Binary packed data as bytes.
        """
        # Convert to specified dtype
        converted = data.astype(self.dtype)
        # Apply endianness if not native
        if self.endian != "=":
            converted = converted.astype(self.endian + converted.dtype.str[1:])
        return converted.tobytes()
    
    def get_extension(self) -> str:
        """Get file extension for binary format.
        
        Returns:
            File extension ".bin".
        """
        return ".bin"
