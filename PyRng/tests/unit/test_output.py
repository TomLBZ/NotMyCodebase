"""Unit tests for output formatters."""

import pytest
import numpy as np
import json
from pyrng.output.formatters import (
    TextFormatter,
    CSVFormatter,
    JSONFormatter,
    BinaryFormatter,
)
from pyrng.core.exceptions import OutputError


class TestTextFormatter:
    """Tests for TextFormatter."""
    
    def test_initialization_with_default_delimiter(self):
        """Test that formatter initializes with default delimiter."""
        formatter = TextFormatter()
        assert formatter.delimiter == "\n"
    
    def test_initialization_with_custom_delimiter(self):
        """Test initialization with custom delimiter."""
        formatter = TextFormatter(delimiter=",")
        assert formatter.delimiter == ","
    
    def test_format_with_newline_delimiter(self, sample_data):
        """Test formatting with newline delimiter."""
        formatter = TextFormatter()
        result = formatter.format(sample_data)
        
        lines = result.split("\n")
        assert len(lines) == len(sample_data)
        assert lines[0] == str(sample_data[0])
    
    def test_format_with_custom_delimiter(self, sample_data):
        """Test formatting with custom delimiter."""
        formatter = TextFormatter(delimiter=",")
        result = formatter.format(sample_data)
        
        values = result.split(",")
        assert len(values) == len(sample_data)
    
    def test_get_extension(self):
        """Test getting file extension."""
        formatter = TextFormatter()
        assert formatter.get_extension() == ".txt"


class TestCSVFormatter:
    """Tests for CSVFormatter."""
    
    def test_initialization_with_defaults(self):
        """Test that formatter initializes with defaults."""
        formatter = CSVFormatter()
        assert formatter.header == "value"
        assert formatter.delimiter == ","
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        formatter = CSVFormatter(header="number", delimiter=";")
        assert formatter.header == "number"
        assert formatter.delimiter == ";"
    
    def test_format_with_header(self, sample_data):
        """Test formatting with header."""
        formatter = CSVFormatter(header="values")
        result = formatter.format(sample_data)
        
        lines = result.split("\n")
        assert lines[0] == "values"
        assert len(lines) == len(sample_data) + 1  # +1 for header
    
    def test_format_without_header(self, sample_data):
        """Test formatting without header."""
        formatter = CSVFormatter(header=None)
        result = formatter.format(sample_data)
        
        lines = result.split("\n")
        assert len(lines) == len(sample_data)
    
    def test_get_extension(self):
        """Test getting file extension."""
        formatter = CSVFormatter()
        assert formatter.get_extension() == ".csv"


class TestJSONFormatter:
    """Tests for JSONFormatter."""
    
    def test_initialization_with_defaults(self):
        """Test that formatter initializes with defaults."""
        formatter = JSONFormatter()
        assert formatter.pretty is False
        assert formatter.include_metadata is False
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        formatter = JSONFormatter(pretty=True, include_metadata=True)
        assert formatter.pretty is True
        assert formatter.include_metadata is True
    
    def test_format_as_array(self, sample_data):
        """Test formatting as JSON array."""
        formatter = JSONFormatter()
        result = formatter.format(sample_data)
        
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) == len(sample_data)
    
    def test_format_with_metadata(self, sample_data):
        """Test formatting with metadata."""
        formatter = JSONFormatter(include_metadata=True)
        result = formatter.format(sample_data)
        
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "data" in parsed
        assert "metadata" in parsed
        assert "count" in parsed["metadata"]
        assert "min" in parsed["metadata"]
        assert "max" in parsed["metadata"]
        assert "mean" in parsed["metadata"]
        assert "std" in parsed["metadata"]
        assert parsed["metadata"]["count"] == len(sample_data)
    
    def test_format_pretty(self, sample_data):
        """Test pretty formatting."""
        formatter = JSONFormatter(pretty=True)
        result = formatter.format(sample_data)
        
        # Pretty printed JSON should have indentation
        assert "  " in result or "\t" in result
        # Should be parseable
        parsed = json.loads(result)
        assert isinstance(parsed, list)
    
    def test_get_extension(self):
        """Test getting file extension."""
        formatter = JSONFormatter()
        assert formatter.get_extension() == ".json"


class TestBinaryFormatter:
    """Tests for BinaryFormatter."""
    
    def test_initialization_with_defaults(self):
        """Test that formatter initializes with defaults."""
        formatter = BinaryFormatter()
        assert formatter.dtype == "float64"
        assert formatter.endian == "<"
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        formatter = BinaryFormatter(dtype="float32", endian=">")
        assert formatter.dtype == "float32"
        assert formatter.endian == ">"
    
    def test_invalid_dtype_raises_error(self):
        """Test that invalid dtype raises OutputError."""
        with pytest.raises(OutputError, match="Invalid dtype"):
            BinaryFormatter(dtype="invalid")
    
    def test_invalid_endian_raises_error(self):
        """Test that invalid endian raises OutputError."""
        with pytest.raises(OutputError, match="Invalid endian"):
            BinaryFormatter(endian="X")
    
    def test_format_returns_bytes(self, sample_data):
        """Test that format returns bytes."""
        formatter = BinaryFormatter()
        result = formatter.format(sample_data)
        
        assert isinstance(result, bytes)
    
    def test_format_with_float64(self, sample_data):
        """Test formatting with float64."""
        formatter = BinaryFormatter(dtype="float64")
        result = formatter.format(sample_data)
        
        # Each float64 is 8 bytes
        assert len(result) == len(sample_data) * 8
    
    def test_format_with_float32(self, sample_data):
        """Test formatting with float32."""
        formatter = BinaryFormatter(dtype="float32")
        result = formatter.format(sample_data)
        
        # Each float32 is 4 bytes
        assert len(result) == len(sample_data) * 4
    
    def test_format_and_decode(self, sample_data):
        """Test that formatted data can be decoded back."""
        formatter = BinaryFormatter(dtype="float64", endian="<")
        result = formatter.format(sample_data)
        
        # Decode back to array
        decoded = np.frombuffer(result, dtype=np.dtype('<f8'))
        assert np.allclose(decoded, sample_data)
    
    def test_get_extension(self):
        """Test getting file extension."""
        formatter = BinaryFormatter()
        assert formatter.get_extension() == ".bin"
