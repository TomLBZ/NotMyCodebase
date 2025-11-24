"""Unit tests for validation utilities."""

import pytest
from pyrng.utils.validation import (
    validate_sample_size,
    validate_positive,
    validate_probability,
    validate_range,
)
from pyrng.core.exceptions import ValidationError


class TestValidateSampleSize:
    """Tests for validate_sample_size function."""
    
    def test_valid_sample_size(self):
        """Test that valid sample sizes pass validation."""
        validate_sample_size(1)
        validate_sample_size(100)
        validate_sample_size(1000000)
    
    def test_zero_sample_size_raises_error(self):
        """Test that zero sample size raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_sample_size(0)
    
    def test_negative_sample_size_raises_error(self):
        """Test that negative sample size raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_sample_size(-5)
    
    def test_non_integer_sample_size_raises_error(self):
        """Test that non-integer sample size raises ValidationError."""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_sample_size(10.5)
        
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_sample_size("10")


class TestValidatePositive:
    """Tests for validate_positive function."""
    
    def test_valid_positive_values(self):
        """Test that positive values pass validation."""
        validate_positive(1, "test")
        validate_positive(0.5, "test")
        validate_positive(1000.0, "test")
    
    def test_zero_raises_error(self):
        """Test that zero raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive(0, "test")
    
    def test_negative_raises_error(self):
        """Test that negative values raise ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive(-1.5, "test")
    
    def test_non_numeric_raises_error(self):
        """Test that non-numeric values raise ValidationError."""
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_positive("1.5", "test")


class TestValidateProbability:
    """Tests for validate_probability function."""
    
    def test_valid_probabilities(self):
        """Test that valid probabilities pass validation."""
        validate_probability(0.0)
        validate_probability(0.5)
        validate_probability(1.0)
    
    def test_probability_greater_than_one_raises_error(self):
        """Test that p > 1 raises ValidationError."""
        with pytest.raises(ValidationError, match="must be between 0 and 1"):
            validate_probability(1.5)
    
    def test_negative_probability_raises_error(self):
        """Test that p < 0 raises ValidationError."""
        with pytest.raises(ValidationError, match="must be between 0 and 1"):
            validate_probability(-0.1)
    
    def test_non_numeric_probability_raises_error(self):
        """Test that non-numeric probability raises ValidationError."""
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_probability("0.5")


class TestValidateRange:
    """Tests for validate_range function."""
    
    def test_valid_ranges(self):
        """Test that valid ranges pass validation."""
        validate_range(0, 10)
        validate_range(0.0, 1.0)
        validate_range(-5.0, 5.0)
    
    def test_equal_bounds_raise_error(self):
        """Test that low == high raises ValidationError."""
        with pytest.raises(ValidationError, match="must be less than upper bound"):
            validate_range(5, 5)
    
    def test_inverted_bounds_raise_error(self):
        """Test that low > high raises ValidationError."""
        with pytest.raises(ValidationError, match="must be less than upper bound"):
            validate_range(10, 5)
    
    def test_non_numeric_bounds_raise_error(self):
        """Test that non-numeric bounds raise ValidationError."""
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_range("0", 10)
        
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_range(0, "10")
