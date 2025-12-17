"""
Plan #1
1. Sort the input array `arr`. This aligns the smallest elements of `arr` with the smallest target values (1, 2, ..., N).
   Minimizing the sum of absolute differences between two sets of numbers is achieved when both are sorted.
2. Initialize `operations` counter to 0.
3. Iterate through the sorted array by index `i` from 0 to N-1.
4. For each element, the target value is `i + 1`.
5. Add the absolute difference `abs(arr[i] - target)` to `operations`.
6. Return `operations`.

Example 1:
Input: [3, 2, 1, 4]
Sorted: [1, 2, 3, 4]
Targets: 1, 2, 3, 4
Diffs: |1-1|=0, |2-2|=0, |3-3|=0, |4-4|=0
Total: 0

Example 2:
Input: [4, 1, 4, 2]
Sorted: [1, 2, 4, 4]
Targets: 1, 2, 3, 4
Diffs: |1-1|=0, |2-2|=0, |4-3|=1, |4-4|=0
Total: 1
"""

from typing import List

def min_operations_to_permutation(arr: List[int]) -> int:
    # Reasoning:
    # To minimize the sum of operations, we should map the smallest number in the input
    # to the smallest number in the target permutation (1), the second smallest to (2), and so on.
    # Sorting the array allows us to align arr[i] with the target value (i + 1).

    n = len(arr)
    arr.sort()

    operations = 0
    for i in range(n):
        target = i + 1
        operations += abs(arr[i] - target)

    return operations


# R E A D M E
# DO NOT CHANGE the code below, we use it to grade your submission.
if __name__ == "__main__":
    line = input()
    k = [int(i) for i in line.strip().split()]
    print(min_operations_to_permutation(k))
