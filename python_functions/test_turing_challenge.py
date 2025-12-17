"""
Unit tests for the Turing Coding Challenge Solution.
"""

import unittest
from python_functions.turing_challenge import min_operations


class TestMinOperations(unittest.TestCase):
    """Test cases for the min_operations function."""

    def test_example_1(self):
        """Test with Example 1: [3, 2, 1, 4] -> 0"""
        input_data = [3, 2, 1, 4]
        expected = 0
        self.assertEqual(min_operations(input_data), expected)

    def test_example_2(self):
        """Test with Example 2: [4, 1, 4, 2] -> 1"""
        input_data = [4, 1, 4, 2]
        expected = 1
        self.assertEqual(min_operations(input_data), expected)

    def test_example_3(self):
        """Test with Example 3: [2, 3, 4, 5] -> 4"""
        input_data = [2, 3, 4, 5]
        expected = 4
        self.assertEqual(min_operations(input_data), expected)

    def test_single_element(self):
        """Test with a single element array."""
        # [1] -> 0
        self.assertEqual(min_operations([1]), 0)
        # [5] -> |5 - 1| = 4
        self.assertEqual(min_operations([5]), 4)
        # [-2] -> |-2 - 1| = 3
        self.assertEqual(min_operations([-2]), 3)

    def test_duplicates(self):
        """Test with duplicates."""
        # [1, 1, 1] -> Target [1, 2, 3] -> |1-1| + |1-2| + |1-3| = 0 + 1 + 2 = 3
        self.assertEqual(min_operations([1, 1, 1]), 3)

    def test_negative_numbers(self):
        """Test with negative numbers."""
        # [-1, -2] -> sorted [-2, -1] -> Target [1, 2] -> |-2-1| + |-1-2| = 3 + 3 = 6
        self.assertEqual(min_operations([-1, -2]), 6)

    def test_already_sorted_permutation(self):
        """Test with an already sorted permutation."""
        self.assertEqual(min_operations([1, 2, 3, 4, 5]), 0)

    def test_reverse_sorted_permutation(self):
        """Test with a reverse sorted permutation."""
        self.assertEqual(min_operations([5, 4, 3, 2, 1]), 0)

    def test_large_gap(self):
        """Test with numbers far from the target range."""
        # [10, 20] -> sorted [10, 20] -> Target [1, 2] -> |10-1| + |20-2| = 9 + 18 = 27
        self.assertEqual(min_operations([10, 20]), 27)


if __name__ == '__main__':
    unittest.main()
