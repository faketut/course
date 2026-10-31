

# Question 1:
# Contains Duplicate
# Given an integer array "nums”, return true if any value appears at least twice in the array, and return false if every element is distinct.
 
# Example 1:
# Input: nums = [1,2,3,1]
# Output: true
 
# Example 2:
# Input: nums = [1,2,3,4]
# Output: false
 
# Example 3:
# Input: nums = [1,1,1,3,3,4,3,2,4,2]
# Output: true
 
class Solution:
    def containsDuplicate(self, nums):
        seen=set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False 
num1=[1,2,3,1]
num2=[1,2,3,4]
nums3=[1,1,1,3,3,4,3,2,4,2]
# s=Solution
# print(s.containsDuplicate(s,num1))

# print(s.containsDuplicate(s,num2))

# print(s.containsDuplicate(s,nums3))


# Question 2:
# K most frequent elements
# Given an integer array nums and an integer k, return the k most frequent elements. return the answer in any order. Assume that all possible input will produce a unique answer.
 
# Example 1:
# Input: nums = [1,1,2,2,3,1], k = 2
# Output: [1,2]
 
# Example 2:
# Input: nums = [1], k = 1
# # Output: [1]
# import heapq,Collections
# h = []
# heapq.heappush(h, 3)
# print([heapq.heappop(h) for _ in range(3)])
import heapq
from collections import Counter
class Solution2:
    def tokKFrequent(self,nums,k):
        freq=Counter(nums)
        k = min(k,len(freq))
        heap = []
        for val,cnt in freq.items():
            if len(heap)<k:
                heapq.heappush(heap,(cnt,val))
        
        
        return [val for cnt,val in list([heapq.heappop(heap) for _ in range(k)])]

s2=Solution2    
print(s2.tokKFrequent(s2,[1,1,2,2,3,1],2))

print(s2.tokKFrequent(s2,[1],1))
