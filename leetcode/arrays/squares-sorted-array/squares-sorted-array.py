from typing import List
from random import randint
from math import floor
import datetime


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        quicksort_start_time = datetime.datetime.now()
        self._quicksort([i**2 for i in nums])
        print(
            "Self written Quicksort: --- %s milliseconds ---"
            % ((datetime.datetime.now() - quicksort_start_time).microseconds / 1000)
        )

        timsort_start_time = datetime.datetime.now()
        [i**2 for i in nums].sort()
        print(
            "Timsort .sort(): --- %s milliseconds ---"
            % ((datetime.datetime.now() - timsort_start_time).microseconds / 1000)
        )

        insertsort_fast_start_time = datetime.datetime.now()
        self._insertsort_fast([i**2 for i in nums])
        print(
            "Fast Self written Insertion Sort: --- %s milliseconds ---"
            % ((datetime.datetime.now() - insertsort_fast_start_time).microseconds / 1000)
        )

        insertsort_slow_start_time = datetime.datetime.now()
        self._insertsort_slow([i**2 for i in nums])
        print(
            "Slow Self written Insertion Sort: --- %s milliseconds ---"
            % ((datetime.datetime.now() - insertsort_slow_start_time).microseconds / 1000)
        )

        merge_sort_start_time = datetime.datetime.now()
        self._mergesort([i**2 for i in nums])
        print(
            "Self written Merge Sort: --- %s milliseconds ---"
            % ((datetime.datetime.now() - merge_sort_start_time).microseconds / 1000)
        )

        return nums

    def _quicksort(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums

        pivot = nums[randint(0, len(nums) - 1)]

        return (
            self._quicksort(nums=[i for i in nums if i < pivot])
            + [i for i in nums if i == pivot]
            + self._quicksort(nums=[i for i in nums if i > pivot])
        )

    def _timsort(self, nums: List[int]) -> List[int]:
        return nums

    def _insertsort_slow(self, nums: List[int]) -> List[int]:
        currentIndex = 0

        if len(nums) < 2:
            return nums

        while currentIndex < len(nums) - 1:
            tempIndex = currentIndex

            while nums[tempIndex] > nums[tempIndex + 1] and tempIndex >= 0:
                # swap elements
                nums[tempIndex] = nums[tempIndex] + nums[tempIndex + 1]
                nums[tempIndex + 1] = nums[tempIndex] - nums[tempIndex + 1]
                nums[tempIndex] = nums[tempIndex] - nums[tempIndex + 1]

                tempIndex -= 1

            currentIndex += 1

        return nums

    def _insertsort_fast(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            currentElement = nums[i]
            j = i - 1

            while currentElement < nums[j] and j >= 0:
                nums[j + 1] = nums[j]
                j -= 1

            nums[j + 1] = currentElement

        return nums

    def _mergesort(self, nums: List[int]) -> List[int]:
        if len(nums) < 2:
            return nums

        pivot_index = floor(len(nums) / 2)
        sorted_first_half_sub_array = self._mergesort(nums[0:pivot_index])
        sorted_second_half_sub_array = self._mergesort(nums[pivot_index : len(nums)])

        i = j = k = 0

        while i < len(sorted_first_half_sub_array) and j < len(sorted_second_half_sub_array):
            if sorted_first_half_sub_array[i] <= sorted_second_half_sub_array[j]:
                nums[k] = sorted_first_half_sub_array[i]
                i += 1
            else:
                nums[k] = sorted_second_half_sub_array[j]
                j += 1
            k += 1

        while i < len(sorted_first_half_sub_array):
            nums[k] = sorted_first_half_sub_array[i]
            i += 1
            k += 1

        while j < len(sorted_second_half_sub_array):
            nums[k] = sorted_second_half_sub_array[j]
            j += 1
            k += 1

        return nums


sol = Solution()

# print(sol.sortedSquares([-4, -1, 0, 3, 10]))
sol.sortedSquares(list(range(-1000, 1000)))
