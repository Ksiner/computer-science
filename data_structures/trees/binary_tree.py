from typing import TypeVar, Generic, Union
from .types import BinaryTreeNode

T = TypeVar("T")


class BinaryTreeBase(Generic[T]):
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

    @property
    def height(self) -> int:
        return self._find_height(self.root)

    def find_node_by_value(self, value: T) -> Union[BinaryTreeNode[T], None]:
        return self.deep_first_search(value=value, node=self.root)

    def deep_first_search(
        self, value: T, node: Union[BinaryTreeNode[T], None] = None
    ) -> Union[BinaryTreeNode[T], None]:
        if not node:
            return None

        if node.value == value:
            return node

        return self.deep_first_search(value=value, node=node.left) or self.deep_first_search(
            value=value, node=node.right
        )

    def _find_height(self, node: Union[BinaryTreeNode[T], None] = None, init_height: int = 0) -> int:
        if not node or not (node.left or node.right):
            return init_height

        next_height = init_height + 1

        return max(
            self._find_height(node.left, init_height=next_height),
            self._find_height(node.right, init_height=next_height),
        )


class OrderedBinaryTree(Generic[T], BinaryTreeBase[T]):
    def traverse_tree(self):
        return self.traverse_sub_tree(self._root)

    def find_successor_by_value(self, value: T) -> Union[BinaryTreeNode[T], None]:
        target_node = self.find_node_by_value(value=value)

        return self.find_successor(node=target_node)

    def find_predecessor_by_value(self, value: T) -> Union[BinaryTreeNode[T], None]:
        target_node = self.find_node_by_value(value=value)

        return self.find_predecessor(node=target_node)

    def traverse_sub_tree(self, node: Union[BinaryTreeNode[T], None]) -> list[BinaryTreeNode[T]]:
        if not node:
            return []

        return (
            (self.traverse_sub_tree(node.left) if node.left else [])
            + [node]
            + (self.traverse_sub_tree(node.right) if node.right else [])
        )

    def find_first_subtree_node(self, node: Union[BinaryTreeNode[T], None] = None):
        if not node:
            return None

        if node.left:
            return self.find_first_subtree_node(node=node.left)

        return node

    def find_last_subtree_node(self, node: Union[BinaryTreeNode[T], None] = None):
        if not node:
            return None

        if node.right:
            return self.find_last_subtree_node(node=node.right)

        return node

    def _find_first_entrance_as_left_subtree(self, node: Union[BinaryTreeNode[T], None] = None):
        """Returns first parent that that contains provided node's subtree as it's left node"""
        if not node:
            return None

        if not node.parent:
            return None

        if node.parent.left == node:
            return node.parent

        return self._find_first_entrance_as_left_subtree(node.parent)

    def find_successor(self, node: Union[BinaryTreeNode[T], None] = None) -> Union[BinaryTreeNode[T], None]:
        if not node:
            return None

        # Root Node case
        if node.right:
            return self.find_first_subtree_node(node.right)

        return self._find_first_entrance_as_left_subtree(node)

    def find_predecessor(self, node: Union[BinaryTreeNode[T], None] = None) -> Union[BinaryTreeNode[T], None]:
        if not node:
            return None

        if node.left:
            return self.find_last_subtree_node(node.left)

        if node.parent and node.parent.right == node:
            return node.parent

        return None

    def __len__(self) -> int:
        return len(self.traverse_tree())
