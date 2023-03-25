function merge(nums1, m, nums2, n) {
  nums1 = mergeSort([...nums1.slice(0, m), ...nums2]);
  console.log(nums1);
};

function mergeSort(array) {
  if (array.length === 1) {
    return array;
  }
  
  let middleIndex = Math.ceil(array.length / 2);
  
  let sortedSubArray1 = mergeSort(array.slice(0, middleIndex));
  let sortedSubArray2 = mergeSort(array.slice(middleIndex, array.length));
  
  let sortedArray = [];
  let subArray1Index = 0;
  let subArray2Index = 0;
  
  while (subArray1Index < sortedSubArray1.length || subArray2Index < sortedSubArray2.length) {
    if (sortedSubArray2[subArray2Index] === undefined) {
      sortedArray.push(sortedSubArray1[subArray1Index]);
      subArray1Index++;
    } else if (sortedSubArray1[subArray1Index] === undefined) {
      sortedArray.push(sortedSubArray2[subArray2Index]);
      subArray2Index++;
    } else if (sortedSubArray1[subArray1Index] <= sortedSubArray2[subArray2Index]) {
      sortedArray.push(sortedSubArray1[subArray1Index]);
      subArray1Index++;
    } else {
      sortedArray.push(sortedSubArray2[subArray2Index]);
      subArray2Index++;
    }
  }
  
  return sortedArray;
}

merge(
  [1,2,3,0,0,0],
  3,
  [2,5,6],
  3,
);