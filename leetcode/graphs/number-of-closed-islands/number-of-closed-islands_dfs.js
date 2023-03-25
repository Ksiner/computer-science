/**
 * @param {number[][]} grid
 * @return {number}
 */
var closedIsland = function(grid) {
  const knownNodes = grid.map(row => row.map(() => false));
  let numClosedIslands = 0;

  for(let yPos = 0; yPos < grid.length; yPos++) {
    for(let xPos = 0; xPos < grid[0].length; xPos++) {
      if (grid[yPos][xPos] === 0 && !knownNodes[yPos][xPos]) {
        let isClosedIsland = dfs(grid, yPos, xPos, knownNodes);

        if (isClosedIsland) {
          numClosedIslands++;
        }
      }
    }
  }

  return numClosedIslands;
};

function dfs(grid, yPos, xPos, knownNodes) {
  let adjacents = [];
  knownNodes[yPos][xPos] = true;
  let surroundedByWater = true;

  // 4-directional adjacents check
  // top direction
  if (isWithinBoundries(yPos - 1, xPos, grid.length - 1, grid[0].length - 1)) {
    if (grid[yPos - 1][xPos] === 0) {
      adjacents.push([yPos - 1, xPos]);
    }
  } else {
    surroundedByWater = false;
  }

  // right direction
  if (isWithinBoundries(yPos, xPos + 1, grid.length - 1, grid[0].length - 1)) {
    if (grid[yPos][xPos + 1] === 0) {
      adjacents.push([yPos, xPos + 1]);
    }
  } else {
    surroundedByWater = false;
  }

  // bottom direction
  if (isWithinBoundries(yPos + 1, xPos, grid.length - 1, grid[0].length - 1)) {
    if (grid[yPos + 1][xPos] === 0) {
      adjacents.push([yPos + 1, xPos]);
    }
  } else {
    surroundedByWater = false;
  }

  // left direction
  if (isWithinBoundries(yPos, xPos - 1, grid.length - 1, grid[0].length - 1)) {
    if (grid[yPos][xPos - 1] === 0) {
      adjacents.push([yPos, xPos - 1]);
    }
  } else {
    surroundedByWater = false;
  }

  for(let i = 0; i < adjacents.length; i++) {
    if (!knownNodes[adjacents[i][0]][adjacents[i][1]]) {
      const subgraphSurroundedByWater = dfs(grid, adjacents[i][0], adjacents[i][1], knownNodes);

      surroundedByWater = surroundedByWater === false ? surroundedByWater : subgraphSurroundedByWater;
    }
  }

  return surroundedByWater;
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


let testGrid = [
  [0,0,1,1,0,1,0,0,1,0],
  [1,1,0,1,1,0,1,1,1,0],
  [1,0,1,1,1,0,0,1,1,0],
  [0,1,1,0,0,0,0,1,0,1],
  [0,0,0,0,0,0,1,1,1,0],
  [0,1,0,1,0,1,0,1,1,1],
  [1,0,1,0,1,1,0,0,0,1],
  [1,1,1,1,1,1,0,0,0,0],
  [1,1,1,0,0,1,0,1,0,1],
  [1,1,1,0,1,1,0,1,1,0]
];


console.log(closedIsland(testGrid));
