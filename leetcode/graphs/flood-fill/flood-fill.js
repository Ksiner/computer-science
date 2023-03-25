function floodFill(image, verticalIndex, horizontalIndex, newColor) {
  const queue = [[verticalIndex, horizontalIndex]];
  const prevColor = image[verticalIndex][horizontalIndex];

  if (prevColor === newColor) {
    return image;
  }

  image[verticalIndex][horizontalIndex] = newColor;

  while (queue.length > 0) {
    const [verticalIndex, horizontalIndex] = queue.shift();

    // Checking top neighbor
    if (isValidNeighbor(image, verticalIndex - 1, horizontalIndex, prevColor, newColor)) {
      queue.push([verticalIndex - 1, horizontalIndex]);
      image[verticalIndex - 1][horizontalIndex] = newColor;
    }

    // Checking right neighbor
    if (isValidNeighbor(image, verticalIndex, horizontalIndex + 1, prevColor, newColor)) {
      queue.push([verticalIndex, horizontalIndex + 1]);
      image[verticalIndex][horizontalIndex + 1] = newColor;
    }

    // Checking bottom neighbor
    if (isValidNeighbor(image, verticalIndex + 1, horizontalIndex, prevColor, newColor)) {
      queue.push([verticalIndex + 1, horizontalIndex]);
      image[verticalIndex + 1][horizontalIndex] = newColor;
    }

    // Checking left neighbor
    if (isValidNeighbor(image, verticalIndex, horizontalIndex - 1, prevColor, newColor)) {
      queue.push([verticalIndex, horizontalIndex - 1]);
      image[verticalIndex][horizontalIndex - 1] = newColor;
    }
  }

  return image;
};

function isValidNeighbor(image, verticalIndex, horizontalIndex, prevColor, newColor) {
  const verticalIndexLimit = image.length - 1;
  const horizontalIndexLimit = image[0].length - 1;

  if (verticalIndex < 0 || verticalIndex > verticalIndexLimit) {
    return false;
  }

  if (horizontalIndex < 0 || horizontalIndex > horizontalIndexLimit) {
    return false;
  }

  if (image[verticalIndex][horizontalIndex] !== prevColor) {
    return false;
  }

  if (image[verticalIndex][horizontalIndex] === newColor) {
    return false;
  }

  return true;
}

// image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2

const result = floodFill([[0,0,0],[0,1,0]], 1, 1, 2);

console.log(result);