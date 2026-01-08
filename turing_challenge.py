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

Plan #2
1. Instead of sorting `arr` in-place, create a sorted copy `sorted_arr`.
   This avoids side effects on the input list, which can be critical if the caller reuses the list.
2. The rest of the logic remains the same as Plan #1.
"""

from typing import List

def min_operations_to_permutation(arr: List[int]) -> int:
    # Reasoning:
    # To minimize the sum of operations, we should map the smallest number in the input
    # to the smallest number in the target permutation (1), the second smallest to (2), and so on.
    # Sorting the array allows us to align arr[i] with the target value (i + 1).

    # Previous approach (Plan #1):
    # n = len(arr)
    # arr.sort() # Modifies input in-place
    # operations = 0
    # for i in range(n):
    #     target = i + 1
    #     operations += abs(arr[i] - target)
    # return operations

    # New approach (Plan #2):
    # Avoid modifying the input array in-place.
    n = len(arr)
    sorted_arr = sorted(arr) # Creates a new list

    operations = 0
    for i in range(n):
        target = i + 1
        operations += abs(sorted_arr[i] - target)

    return operations

"""
Test Cases Verification:
1. Example 1: [3, 2, 1, 4] -> Sorted [1, 2, 3, 4] -> Target [1, 2, 3, 4] -> Cost 0. PASSED.
2. Example 2: [4, 1, 4, 2] -> Sorted [1, 2, 4, 4] -> Target [1, 2, 3, 4] -> Cost 1. PASSED.
3. Example 3: [2, 3, 4, 5] -> Sorted [2, 3, 4, 5] -> Target [1, 2, 3, 4] -> Cost 4. PASSED.
4. Empty Input: [] -> n=0, loop doesn't run -> Cost 0. PASSED.
5. Single Element: [1] -> Sorted [1] -> Target [1] -> Cost 0. PASSED.
6. Single Element (Large): [10] -> Sorted [10] -> Target [1] -> Cost 9. PASSED.
7. Single Element (Negative): [-5] -> Sorted [-5] -> Target [1] -> Cost 6. PASSED.
8. Duplicates: [1, 1] -> Sorted [1, 1] -> Target [1, 2] -> Cost |1-1| + |1-2| = 1. PASSED.
9. Large Numbers: [100, 200] -> Sorted [100, 200] -> Target [1, 2] -> Cost |99| + |198| = 297. PASSED.
10. Side Effect Check: Verified that the original array is not modified by the function. PASSED.
"""

# R E A D M E
# DO NOT CHANGE the code below, we use it to grade your submission.
if __name__ == "__main__":
    line = input()
    k = [int(i) for i in line.strip().split()]
    print(min_operations_to_permutation(k))
