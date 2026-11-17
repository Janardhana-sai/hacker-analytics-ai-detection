"""
Sample: Idiomatic Human Senior Python Engineer Implementation.
Clean pythonic syntax, concise logic, minimal textbook scaffolding.
"""

from itertools import accumulate


def two_sum_fast(numbers, target):
    lookup = {}
    for idx, num in enumerate(numbers):
        if target - num in lookup:
            return lookup[target - num], idx
        lookup[num] = idx
    return None


def max_subarray_kadane(nums):
    if not nums:
        raise ValueError("nums must not be empty")

    best = current = nums[0]
    for x in nums[1:]:
        current = x if current < 0 else current + x
        if current > best:
            best = current
    return best


def find_anagram_groups(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())

