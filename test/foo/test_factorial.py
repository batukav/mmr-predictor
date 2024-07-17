import sys
import os
import pytest

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from foo.factorial import calculate_factorial


# Tests

def test_factorial_invalid():
    with pytest.raises(ValueError):
        calculate_factorial(-1)
    
def test_factorial_lower():
    assert calculate_factorial(0) == 1
    assert calculate_factorial(1) == 1
    
def test_factorial_upper():
    assert calculate_factorial(6) == 720