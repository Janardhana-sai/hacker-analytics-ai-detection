"""
Sample Python implementation 1: Two-Sum & Subarray Analytics Utility.
Structured style with docstrings, type hints, and step-by-step comments.
"""

from typing import List, Optional, Tuple


def find_two_sum_indices(numbers: List[int], target_value: int) -> Optional[Tuple[int, int]]:
    """
    Find indices of two numbers in the list that add up to the target value.

    Args:
        numbers: List of integer values.
        target_value: Desired sum value.

    Returns:
        A tuple containing the two indices if found, otherwise None.
    """
    # Step 1: Initialize dictionary to store visited values and their indices
    seen_values: dict[int, int] = {}

    # Step 2: Iterate through each element with its index
    for current_index, current_value in enumerate(numbers):
        # Step 3: Compute the complement needed to reach target_value
        complement = target_value - current_value

        # Step 4: Check if the complement has already been encountered
        if complement in seen_values:
            return seen_values[complement], current_index

        # Step 5: Store the current value and index for future lookups
        seen_values[current_value] = current_index

    # Step 6: Return None when no valid pair exists
    return None


def calculate_maximum_subarray_sum(values: List[int]) -> int:
    """
    Compute the maximum contiguous subarray sum using Kadane's algorithm.

    Args:
        values: Non-empty list of integers.

    Returns:
        Maximum sum of a contiguous subarray.
    """
    if not values:
        raise ValueError("Input list must contain at least one integer.")

    # Initialize tracking variables with the first element
    current_sum = values[0]
    best_sum = values[0]

    # Traverse remaining elements to update running and global maximums
    for value in values[1:]:
        current_sum = max(value, current_sum + value)
        best_sum = max(best_sum, current_sum)

    return best_sum


if __name__ == "__main__":
    sample_nums = [2, 7, 11, 15]
    print("Two sum:", find_two_sum_indices(sample_nums, 9))
    print("Max subarray:", calculate_maximum_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))

