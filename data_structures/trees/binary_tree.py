from typing import TypeVar, Generic, Union
from .types import BinaryTreeNode

T = TypeVar("T")


class BinaryTree(Generic[T]):
    def __init__(self, root: Union[BinaryTreeNode[T], None] = None) -> None:
        self._root = root

    @property
    def root(self):
        self._len = None
        self._height = None
        return self._root

    @root.setter
    def root(self, new_root: Union[BinaryTreeNode[T], None]):
        self._root = new_root

        return self._root

    def traverse(self):
        return self._traverse_in_order(self._root)

    def _traverse_in_order(self, node: Union[BinaryTreeNode[T], None]) -> list[BinaryTreeNode[T]]:
        results: list[BinaryTreeNode[T]] = []

        if not node:
            return results

        results = results + self._traverse_in_order(node.left)
        results.append(node)
        results = results + self._traverse_in_order(node.right)

        return results

    def _find_height(self, node: Union[BinaryTreeNode[T], None] = None, init_height: int = 0) -> int:
        if not node or not (node.left or node.right):
            return init_height

        next_height = init_height + 1

        return max(
            self._find_height(node.left, init_height=next_height),
            self._find_height(node.right, init_height=next_height),
        )

    def __len__(self) -> int:
        return len(self.traverse())

    @property
    def height(self) -> int:
        return self._find_height(self.root)
