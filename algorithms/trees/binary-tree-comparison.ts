type NodeType = {
  value: any;
  left?: NodeType
  right?: NodeType
}


function compare_binary_tree_recursion(a?: NodeType, b?: NodeType): boolean {
  if (!a && !b) {
    return true
  }

  if (!a || !b) {
    return false
  }

  if (a.value !== b.value) {
    return false
  }

  return compare_binary_tree_recursion(a.left, b.left) && compare_binary_tree_recursion(a.right, b.right)
}

function compare_binary_tree_cycle(a?: NodeType, b?: NodeType): boolean {
  const aQueue = [a]
  const bQueue = [b]

  while (aQueue.length && bQueue.length) {
    let currentA = aQueue.shift();
    let currentB = bQueue.shift();

    if (!currentA && !currentB) {
      continue;
    }

    if (!currentA || !currentB) {
      return false
    }

    if (currentA.value !== currentB.value) {
      return false
    }

    aQueue.push(currentA.left, currentA.right)
    bQueue.push(currentB.left, currentB.right)
  }

  return aQueue.length === bQueue.length
}

const testData = {
  a: {
    value: 1,
    left: {
      value: 2,
    },
    right: {
      value: 3,
    },
  } as NodeType,

  b: {
    value: 1,
    left: {
      value: 2,
    },
    right: {
      value: 3,
    }
  } as NodeType
}

console.log(compare_binary_tree_recursion(testData.a, testData.b))
console.log(compare_binary_tree_cycle(testData.a, testData.b))