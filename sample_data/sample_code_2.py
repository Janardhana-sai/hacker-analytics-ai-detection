# Sample Python implementation 2: Alternate algorithm style for comparison

def two_sum(arr, target):
    lookup = {}
    for i, x in enumerate(arr):
        diff = target - x
        if diff in lookup:
            return (lookup[diff], i)
        lookup[x] = i
    return None


def max_subarray(nums):
    if len(nums) == 0:
        raise ValueError("empty array")
    curr = nums[0]
    ans = nums[0]
    for k in range(1, len(nums)):
        if curr + nums[k] > nums[k]:
            curr = curr + nums[k]
        else:
            curr = nums[k]
        if curr > ans:
            ans = curr
    return ans


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))
    print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))

