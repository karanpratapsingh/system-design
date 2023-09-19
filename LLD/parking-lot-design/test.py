from collections import deque

def maxSlidingWindow(nums, k):
    min_ = min(nums[0:k])
    res = [min_]
    for i in range(k, len(nums)):
        if nums[i - k] == min_:
            min_ = min(nums[i - k + 1:i + 1])
        elif nums[i] < min_:
            min_ = nums[i]

        res.append(min_)

    return max(res)

print(maxSlidingWindow([1,2, 3,1, 2], 2))