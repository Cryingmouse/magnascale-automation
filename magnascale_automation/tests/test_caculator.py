# test_calculator.py

import unittest

from ddt import data
from ddt import ddt
from ddt import unpack


def add(a, b):
    """Returns the sum of two numbers."""
    return a + b


@ddt
class TestCalculator(unittest.TestCase):
    """Unit tests for the add function."""

    @data(
        (1, 2, 3),  # Test case 1: 1 + 2 = 3
        (-1, 1, 0),  # Test case 2: -1 + 1 = 0
        (0, 0, 0),  # Test case 3: 0 + 0 = 0
        (1.5, 2.5, 4.0),  # Test case 4: 1.5 + 2.5 = 4.0
    )
    @unpack
    def test_add(self, a, b, expected):
        """Test add function with various inputs."""
        self.assertEqual(add(a, b), expected)
