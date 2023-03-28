from typing import TypeVar, Generic, Union, Any

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

        if self._left:
            self._left.parent = self

        if self._right:
            self._right.parent = self

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

        return self._left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_right: Union["BinaryTreeNode[T]", None]):
        self._right = new_right

        if self._right:
            self._right._parent = self

        return self._right

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Union["BinaryTreeNode[T]", None]):
        self._parent = parent

        return self._parent

    def delete_child(self, node: Union["BinaryTreeNode[T]", None]) -> "BinaryTreeNode[T]":
        if not node:
            return self

        if self.left == node:
            self.left = None

        if self.right == node:
            self.right = None

        return self

    def __repr__(self) -> str:
        return str(self.value)
