var searchInsert = function(nums, target) {
  let startIndex = 0;
  let endIndex = nums.length - 1;

  if (target < nums[0]) {
      return 0;
  }

  if (nums[endIndex] < target) {
      return endIndex + 1;
  }
  

  while(startIndex <= endIndex) {
    let pivotIndex = Math.floor((startIndex + endIndex) / 2);

    if (nums[pivotIndex] === target) {
      return pivotIndex
    }

    if (nums[pivotIndex] > target) {
      endIndex = pivotIndex - 1;
    } else {
      startIndex = pivotIndex + 1
    }
  }

  return startIndex
};

console.log('[1,3,5,6], 5', searchInsert([1,3,5,6], 5), searchInsert([1,3,5,6], 5) === 2);
console.log('[1,3,5,6], 2', searchInsert([1,3,5,6], 2), searchInsert([1,3,5,6], 2) === 1);
console.log('[1,3,5,6], 7', searchInsert([1,3,5,6], 7), searchInsert([1,3,5,6], 7) === 4);
console.log('[2,3,4,8,10], 0', searchInsert([2,3,4,8,10], 0), searchInsert([2,3,4,8,10], 0) === 0);