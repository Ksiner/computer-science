/**
 * @param {number[][]} grid1
 * @param {number[][]} grid2
 * @return {number}
 */
var countSubIslands = function(grid1, grid2) {
  const knownNodes = grid2.map(row => row.map(() => false));
  let subIslandsCount = 0;

  for(yPos = 0; yPos < grid2.length; yPos++) {
    for(xPos = 0; xPos < grid2[0].length; xPos++) {
      if (grid2[yPos][xPos] === 1 && !knownNodes[yPos][xPos]) {
        const isSubIslandGraph = dfs(grid1, grid2, yPos, xPos, knownNodes);

        if (isSubIslandGraph) {
          subIslandsCount++;
        }
      }
    }
  }

  return subIslandsCount;
};

function dfs(grid1, grid2, yPos, xPos, knownNodes) {
  knownNodes[yPos][xPos] = true;
  let isSubIsland = grid1[yPos][xPos] === grid2[yPos][xPos];
  let adjacents = [];

  // Checking top neighbor
  if (isValidNeighbor(grid2, yPos - 1, xPos)) {
    adjacents.push([yPos - 1, xPos]);
  }

  // Checking right neighbor
  if (isValidNeighbor(grid2, yPos, xPos + 1)) {
    adjacents.push([yPos, xPos + 1]);
  }

  // Checking bottom neighbor
  if (isValidNeighbor(grid2, yPos + 1, xPos)) {
    adjacents.push([yPos + 1, xPos]);
  }

  // Checking left neighbor
  if (isValidNeighbor(grid2, yPos, xPos - 1)) {
    adjacents.push([yPos, xPos - 1]);
  }

  for (let i = 0; i < adjacents.length; i++) {
    if (!knownNodes[adjacents[i][0]][adjacents[i][1]]) {
      let isSubgraphSubIsland = dfs(grid1, grid2, adjacents[i][0], adjacents[i][1], knownNodes);

      isSubIsland = isSubIsland === false ? false : isSubgraphSubIsland;
    }
  }

  return isSubIsland;
}

function isValidNeighbor(grid, yPos, xPos) {
  const yPosLimit = grid.length - 1;
  const xPosLimit = grid[0].length - 1;
  
  if (yPos < 0 || yPos > yPosLimit) {
    return false;
  }

  if (xPos < 0 || xPos > xPosLimit) {
    return false;
  }

  if (grid[yPos][xPos] !== 1) {
    return false;
  }

  return true;
}

const test1Grid1 = [[1,1,1,0,0],[0,1,1,1,1],[0,0,0,0,0],[1,0,0,0,0],[1,1,0,1,1]];
const test1Grid2 = [[1,1,1,0,0],[0,0,1,1,1],[0,1,0,0,0],[1,0,1,1,0],[0,1,0,1,0]];

const test2Grid1 = [[1,0,1,0,1],[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1],[1,0,1,0,1]];
const test2Grid2 = [[0,0,0,0,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,0,1,0],[1,0,0,0,1]];

console.log(countSubIslands(test1Grid1, test1Grid2));
console.log(countSubIslands(test2Grid1, test2Grid2));