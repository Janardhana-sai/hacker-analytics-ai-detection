# Sample: Student Scratchpad Implementation
# max subarray and two sum quick test

def twoSum(nums, target):
    # loop through all items manually
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def maxSubArray(A):
    if len(A) == 0:
        return 0
    max_so_far = A[0]
    curr_max = A[0]
    # iterate
    for i in range(1, len(A)):
        if curr_max + A[i] > A[i]:
            curr_max = curr_max + A[i]
        else:
            curr_max = A[i]
        if curr_max > max_so_far:
            max_so_far = curr_max
    return max_so_far

