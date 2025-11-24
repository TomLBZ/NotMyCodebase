"""Unit tests for exception classes."""

import pytest
from pyrng.core.exceptions import (
    PyRngError,
    ValidationError,
    DistributionError,
    OutputError,
    ConfigurationError,
    GenerationError,
)


def test_pyrng_error_base():
    """Test that PyRngError is the base exception."""
    error = PyRngError("test error")
    assert isinstance(error, Exception)
    assert str(error) == "test error"


def test_validation_error_inherits_from_base():
    """Test that ValidationError inherits from PyRngError."""
    error = ValidationError("validation failed")
    assert isinstance(error, PyRngError)
    assert isinstance(error, Exception)


def test_distribution_error_inherits_from_base():
    """Test that DistributionError inherits from PyRngError."""
    error = DistributionError("unknown distribution")
    assert isinstance(error, PyRngError)


def test_output_error_inherits_from_base():
    """Test that OutputError inherits from PyRngError."""
    error = OutputError("output failed")
    assert isinstance(error, PyRngError)


def test_configuration_error_inherits_from_base():
    """Test that ConfigurationError inherits from PyRngError."""
    error = ConfigurationError("invalid config")
    assert isinstance(error, PyRngError)


def test_generation_error_inherits_from_base():
    """Test that GenerationError inherits from PyRngError."""
    error = GenerationError("generation failed")
    assert isinstance(error, PyRngError)


def test_exception_chaining():
    """Test that exceptions can be chained properly."""
    try:
        try:
            raise ValueError("original error")
        except ValueError as e:
            raise ValidationError("wrapped error") from e
    except ValidationError as e:
        assert str(e) == "wrapped error"
        assert isinstance(e.__cause__, ValueError)
        assert str(e.__cause__) == "original error"
