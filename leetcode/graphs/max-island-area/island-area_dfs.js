/**
 * @param {number[][]} grid
 * @return {number}
 */
var maxAreaOfIsland = function(grid) {
  const knownNodes = grid.map(row => row.map(() => false));
  let maxGraphLength = 0;

  for(let yPos = 0; yPos < grid.length; yPos++) {
    for(let xPos = 0; xPos < grid[0].length; xPos++) {
      if (grid[yPos][xPos] === 1 && !knownNodes[yPos][xPos]) {
        let graphLength = dfs(grid, yPos, xPos, knownNodes);

        if (maxGraphLength < graphLength) {
          maxGraphLength = graphLength;
        }
      }
    }
  }

  return maxGraphLength;
};

function dfs(grid, yPos, xPos, knownNodes) {
  let adjacents = [];
  knownNodes[yPos][xPos] = true;
  graphLength = 1;

  // 4-directional adjacents check
  // top direction
  if (isAdjacent(grid, yPos - 1, xPos)) {
    adjacents.push([yPos - 1, xPos]);
  }
  // right direction
  if (isAdjacent(grid, yPos, xPos + 1)) {
    adjacents.push([yPos, xPos + 1]);
  }
  // bottom direction
  if (isAdjacent(grid, yPos + 1, xPos)) {
    adjacents.push([yPos + 1, xPos]);
  }
  // left direction
  if (isAdjacent(grid, yPos, xPos - 1)) {
    adjacents.push([yPos, xPos - 1]);
  }

  for(let i = 0; i < adjacents.length; i++) {
    if (!knownNodes[adjacents[i][0]][adjacents[i][1]]) {
      graphLength += dfs(grid, adjacents[i][0], adjacents[i][1], knownNodes);
    }
  }

  return graphLength;
}

function isAdjacent(grid, yPos, xPos) {
  if (yPos < 0 || yPos >= grid.length) {
    return false;
  }

  if (xPos < 0 || xPos >= grid[0].length) {
    return false;
  }

  return grid[yPos][xPos] === 1;
}


let testGrid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]];


console.log(maxAreaOfIsland(testGrid));
