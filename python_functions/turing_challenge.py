"""
Turing Coding Challenge Solution.

Problem:
Given an array of N integers, transform it into a permutation of the first N positive integers.
Operations: Increase or decrease any element by 1.
Goal: Find the minimum number of operations.

Approach:
To minimize the sum of absolute differences between the array elements and the target permutation
(1, 2, ..., N), we should map the smallest element of the input array to the smallest element
of the target permutation, the second smallest to the second smallest, and so on.

Proof of correctness relies on the rearrangement inequality concept (specifically for L1 norm minimization).
"""

from typing import List


def min_operations(n: List[int]) -> int:
    """
    Calculates the minimum number of operations to transform the input array
    into a permutation of 1 to N.

    Args:
        n (List[int]): A list of N integers.

    Returns:
        int: The minimum number of operations required.
    """
    # Sort the input array to align with the target permutation sequence
    n_sorted = sorted(n)

    # The size of the array
    size = len(n)

    operations = 0

    # Iterate through the sorted array and compare with target 1..N
    # We use 0-based index 'i', so the target value for index 'i' is 'i + 1'
    for i in range(size):
        target_value = i + 1
        current_value = n_sorted[i]

        # Add the absolute difference to the total operations count
        operations += abs(current_value - target_value)

    return operations
