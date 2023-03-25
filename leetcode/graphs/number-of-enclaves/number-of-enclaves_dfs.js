/**
 * @param {number[][]} grid
 * @return {number}
 */
var numEnclaves = function(grid) {
  const knownNodes = grid.map(row => row.map(() => false));
  let enclavesCount = 0;

  for(let yPos = 0; yPos < grid.length; yPos++) {
    for(let xPos = 0; xPos < grid[0].length; xPos++) {
      if (grid[yPos][xPos] === 1 && !knownNodes[yPos][xPos]) {
        let graphEnclavesCount = bfs(grid, yPos, xPos, knownNodes);

        enclavesCount += graphEnclavesCount;
      }
    }
  }

  return enclavesCount;
};

function bfs(grid, yPos, xPos, knownNodes) {
  let queue = [];
  let graphLength = 0;
  let hasBoundryNode = false;

  queue.push([yPos, xPos]);
  knownNodes[yPos][xPos] = true;

  while (queue.length > 0) {
    let [yPos, xPos] = queue.shift();
    graphLength++;

    // 4-directional adjacents check
    // top direction
    if (isWithinBoundries(yPos - 1, xPos, grid.length - 1, grid[0].length - 1)) {
      if (grid[yPos - 1][xPos] === 1 && !knownNodes[yPos - 1][xPos]) {
        queue.push([yPos - 1, xPos]);
        knownNodes[yPos - 1][xPos] = true;
      }
    } else {
      hasBoundryNode = true;
    }

    // right direction
    if (isWithinBoundries(yPos, xPos + 1, grid.length - 1, grid[0].length - 1)) {
      if (grid[yPos][xPos + 1] === 1 && !knownNodes[yPos][xPos + 1]) {
        queue.push([yPos, xPos + 1]);
        knownNodes[yPos][xPos + 1] = true;
      }
    } else {
      hasBoundryNode = true;
    }

    // bottom direction
    if (isWithinBoundries(yPos + 1, xPos, grid.length - 1, grid[0].length - 1)) {
      if (grid[yPos + 1][xPos] === 1 && !knownNodes[yPos + 1][xPos]) {
        queue.push([yPos + 1, xPos]);
        knownNodes[yPos + 1][xPos] = true;
      }
    } else {
      hasBoundryNode = true;
    }

    // left direction
    if (isWithinBoundries(yPos, xPos - 1, grid.length - 1, grid[0].length - 1)) {
      if (grid[yPos][xPos - 1] === 1 && !knownNodes[yPos][xPos - 1]) {
        queue.push([yPos, xPos - 1]);
        knownNodes[yPos][xPos - 1] = true;
      }
    } else {
      hasBoundryNode = true;
    }
  }

  return hasBoundryNode ? 0 : graphLength;
}

function isWithinBoundries(yPos, xPos, yMax, xMax) {
  if (yPos < 0 || yPos > yMax) {
    return false;
  }

  if (xPos < 0 || xPos > xMax) {
    return false;
  }

  return true;
}


let testGrid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]];
let testGrid2 = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]];
let testGrid3 = [
  [0,0,0,1,1,1,0,1,0,0],
  [1,1,0,0,0,1,0,1,1,1],
  [0,0,0,1,1,1,0,1,0,0],
  [0,1,1,0,0,0,1,0,1,0],
  [0,1,1,1,1,1,0,0,1,0],
  [0,0,1,0,1,1,1,1,0,1],
  [0,1,1,0,0,0,1,1,1,1],
  [0,0,1,0,0,1,0,1,0,1],
  [1,0,1,0,1,1,0,0,0,0],
  [0,0,0,0,1,1,0,0,0,1]
];
let testGrid4 = [
  [0,0,0,1,1,1,0,1,1,1,1,1,0,0,0],
  [1,1,1,1,0,0,0,1,1,0,0,0,1,1,1],
  [1,1,1,0,0,1,0,1,1,1,0,0,0,1,1],
  [1,1,0,1,0,1,1,0,0,0,1,1,0,1,0],
  [1,1,1,1,0,0,0,1,1,1,0,0,0,1,1],
  [1,0,1,1,0,0,1,1,1,1,1,1,0,0,0],
  [0,1,0,0,1,1,1,1,0,0,1,1,1,0,0],
  [0,0,1,0,0,0,0,1,1,0,0,1,0,0,0],
  [1,0,1,0,0,1,0,0,0,0,0,0,1,0,1],
  [1,1,1,0,1,0,1,0,1,1,1,0,0,1,0]
];


console.log(numEnclaves(testGrid));
console.log(numEnclaves(testGrid2));
console.log(numEnclaves(testGrid3));
console.log(numEnclaves(testGrid4));
