from typing import List


class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        max_turbulence_length = 1

        current_index = 1

        inc = 1
        dec = 1

        while current_index < len(arr):
            if arr[current_index - 1] < arr[current_index]:
                inc = dec + 1
                dec = 1
            elif arr[current_index - 1] > arr[current_index]:
                dec = inc + 1
                inc = 1
            else:
                inc = 1
                dec = 1

            current_index += 1
            max_turbulence_length = max(max_turbulence_length, max(dec, inc))

        return max_turbulence_length


sol = Solution()

print(sol.maxTurbulenceSize([9, 4, 2, 10, 7, 8, 8, 1, 9]))
print(sol.maxTurbulenceSize([0, 8, 45, 88, 48, 68, 28, 55, 17, 24]))
print(sol.maxTurbulenceSize([4, 8, 12, 16]))
print(sol.maxTurbulenceSize([100]))
print(sol.maxTurbulenceSize([100, 100]))
