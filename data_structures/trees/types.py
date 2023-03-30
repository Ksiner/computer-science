from typing import TypeVar, Generic, Union, Any
import json

T = TypeVar("T")


class BinaryTreeNode(Generic[T]):
    def __init__(
        self,
        value: T,
        left: Union["BinaryTreeNode[T]", None] = None,
        right: Union["BinaryTreeNode[T]", None] = None,
    ) -> None:
        self._value = value
        self._parent: Union["BinaryTreeNode[T]", None] = None
        self._left: Union["BinaryTreeNode[T]", None] = left
        self._right: Union["BinaryTreeNode[T]", None] = right
        self._height: int = 0
        self._subtree_size: int = 1

        if self._left:
            self._left.parent = self

        if self._right:
            self._right.parent = self

        self._recalculate_augmentations(self)

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> T:
        self._value = value

        return self._value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_left: Union["BinaryTreeNode[T]", None]):
        self._left = new_left

        if self._left:
            self._left._parent = self

        self._recalculate_augmentations(self)

        return self._left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_right: Union["BinaryTreeNode[T]", None]):
        self._right = new_right

        if self._right:
            self._right._parent = self

        self._recalculate_augmentations(self)

        return self._right

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Union["BinaryTreeNode[T]", None]):
        prev_parent = self._parent

        self._parent = parent

        if parent:
            self._recalculate_augmentations(parent)

        if prev_parent:
            self._recalculate_augmentations(prev_parent)

        return self._parent

    @property
    def height(self):
        return self._height

    @property
    def subtree_size(self):
        return self._subtree_size

    def delete_child(self, node: Union["BinaryTreeNode[T]", None]) -> "BinaryTreeNode[T]":
        if not node:
            return self

        if self.left == node or self.right == node:
            if self.left == node:
                self.left = None

            if self.right == node:
                self.right = None

            self._recalculate_augmentations(self)

        return self

    def _recalculate_augmentations(self, node: "BinaryTreeNode[T]"):
        self._recalculate_subtree_height(node)
        self._recalculate_subtree_size(node)

    def _recalculate_subtree_height(self, node: "BinaryTreeNode[T]"):
        left_subtree_height = node.left.height if node.left else 0
        right_subtree_height = node.right.height if node.right else 0

        new_height = max(left_subtree_height, right_subtree_height) + 1 if node.right or node.left else 0

        if new_height == node.height:
            return

        node._height = new_height

        if node.parent:
            node._recalculate_subtree_height(node.parent)

    def _recalculate_subtree_size(self, node: "BinaryTreeNode[T]"):
        left_subtree_size = node.left._subtree_size if node.left else 0
        right_subtree_size = node.right._subtree_size if node.right else 0

        new_size = (left_subtree_size) + (right_subtree_size) + 1

        if node._subtree_size == new_size:
            return

        node._subtree_size = new_size

        if node.parent:
            self._recalculate_subtree_size(node.parent)

    def __repr__(self) -> str:
        return json.dumps({"value": self.value, "height": self.height, "size": self.subtree_size})
