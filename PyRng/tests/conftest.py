"""Pytest configuration and fixtures."""

import pytest
import numpy as np
from pathlib import Path


@pytest.fixture
def default_rng():
    """Provide a seeded RNG for reproducible tests.
    
    Returns:
        NumPy random generator with fixed seed.
    """
    return np.random.default_rng(seed=42)


@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide a temporary directory for output files.
    
    Args:
        tmp_path: Pytest's temporary directory fixture.
    
    Returns:
        Path to temporary output directory.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_data():
    """Provide sample data for testing output formatters.
    
    Returns:
        NumPy array of sample data.
    """
    return np.array([1.5, 2.7, 3.9, 4.1, 5.3])


@pytest.fixture
def sample_data_large():
    """Provide larger sample data for statistical tests.
    
    Returns:
        NumPy array of 10000 samples.
    """
    rng = np.random.default_rng(seed=42)
    return rng.normal(0, 1, 10000)
