"""
Sample: AI Interview Solution with Object-Oriented Boilerplate.
Class-based wrapper, uniform docstrings, defensive type hints, and auxiliary helper methods.
"""

from typing import List, Optional, Tuple


class ArrayProblemSolver:
    """
    A utility class designed to solve classical algorithmic array problems
    including Two-Sum and Maximum Subarray problems.
    """

    def __init__(self, debug_mode: bool = False) -> None:
        """Initialize the solver with optional debug logging configuration."""
        self.debug_mode: bool = debug_mode
        self.execution_count: int = 0

    def find_two_sum(
        self, numbers_list: List[int], target_value: int
    ) -> Optional[Tuple[int, int]]:
        """
        Locates two numbers in numbers_list that add up to target_value.

        Args:
            numbers_list: List of candidate integers.
            target_value: The target integer sum.

        Returns:
            A tuple containing indices of the two elements, or None.
        """
        # Step 1: Increment internal execution tracker
        self.execution_count += 1

        # Step 2: Initialize lookup hash map
        element_index_lookup: dict[int, int] = {}

        # Step 3: Iterate through elements sequentially
        for current_index, current_value in enumerate(numbers_list):
            complement_needed: int = target_value - current_value

            if complement_needed in element_index_lookup:
                return (element_index_lookup[complement_needed], current_index)

            element_index_lookup[current_value] = current_index

        return None

    def compute_max_subarray(self, input_array: List[int]) -> int:
        """
        Calculates the maximum sum contiguous subarray using Kadane's dynamic strategy.

        Args:
            input_array: Non-empty list of integers.

        Returns:
            The maximum subarray sum integer value.
        """
        if not input_array:
            raise ValueError("Input array must contain at least one element.")

        running_sum: int = input_array[0]
        optimal_sum: int = input_array[0]

        for element in input_array[1:]:
            running_sum = max(element, running_sum + element)
            optimal_sum = max(optimal_sum, running_sum)

        return optimal_sum

