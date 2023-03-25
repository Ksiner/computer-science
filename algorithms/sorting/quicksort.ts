import { random } from 'lodash';

const randArrayLength = random(500, 1000, false);

const testArray = Array.apply(null, Array(randArrayLength)).map(() => random(100000, false));

const quicksort = (array: number[]) => {
  if (array.length <= 1) {
    return array;
  }

  const pivot = array[random(0, array.length - 1, false)];

  const partitionThatIsLessThanPivot = array.filter(value => value < pivot);
  const partitionThatIsGreaterThanPivot = array.filter(value => value > pivot);

  return [...quicksort(partitionThatIsLessThanPivot), pivot, ...quicksort(partitionThatIsGreaterThanPivot)];
}

console.log('Unordered array', testArray, testArray.length);
console.log('Array ordered with quicksort', quicksort(testArray));