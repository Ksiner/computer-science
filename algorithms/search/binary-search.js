function search(nums, target) {
  let subArrayStart = 0;
  let subArrayEndIndex = nums.length;
  
  while(true) {
    let subArrayLength = subArrayEndIndex - subArrayStart;
    let pivotElementIndex = getPivotIndex(subArrayLength) + subArrayStart;
    let pivotElement = nums[pivotElementIndex];
    
    if (pivotElement === target) {
      return pivotElementIndex
    }

    if (subArrayLength <= 1) {
      return -1;
    }

    if (pivotElement > target) {
      subArrayEndIndex = pivotElementIndex;
      continue;
    }

    subArrayStart = pivotElementIndex + 1;
  }
};

function getPivotIndex(arrayLength) {
  return Math.floor((arrayLength - 1) / 2);
}

console.log(search([-1, 0, 5], -1));