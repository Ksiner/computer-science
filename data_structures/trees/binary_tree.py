from typing import TypeVar, Generic, Union
from .types import BinaryTreeNode
from collections import deque
from graphviz import Graph

T = TypeVar("T")


class BinaryTreeBase(Generic[T]):
    def __init__(self, root: Union[BinaryTreeNode[T], None] = None) -> None:
        self._root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, new_root: Union[BinaryTreeNode[T], None]):
        self._root = new_root

        return self._root

    @property
    def height(self) -> int:
        return self._root.height if self._root else 0

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

    def _recalculate_node_height(self, node: "BinaryTreeNode[T]"):
        if not (node.right or node.left):
            node._height = 0
            return

        new_height = max(node.left._height if node.left else 0, node.right._height if node.right else 0) + 1

        if new_height == node.height:
            return

        node._height = new_height

        if node.parent:
            self._recalculate_node_height(node.parent)


class OrderedBinaryTree(Generic[T], BinaryTreeBase[T]):
    def __init__(self, root: Union[BinaryTreeNode[T], None] = None) -> None:
        super().__init__(root)
        self._root = root

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

    def find_by_index(self, index: int) -> Union[BinaryTreeNode[T], None]:
        if not self._root or self._root.subtree_size <= index or index < 0:
            return None

        return self._search_by_index_in_subtree(node=self._root, index=index)

    def _search_by_index_in_subtree(self, node: BinaryTreeNode[T], index: int) -> Union[BinaryTreeNode[T], None]:
        left_subtree_size = node.left.subtree_size if node.left else 0

        if index == left_subtree_size:
            return node
        elif index < left_subtree_size and node.left:
            # searching in the left subtree
            return self._search_by_index_in_subtree(node=node.left, index=index)
        elif index > left_subtree_size and node.right:
            return self._search_by_index_in_subtree(node=node.right, index=(index - left_subtree_size - 1))

        return None

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

    def insert_after_by_value(self, value: T, after_value: T) -> Union[BinaryTreeNode[T], None]:
        node_after = self.find_node_by_value(value=after_value)

        return self.insert_after(value=value, after_node=node_after)

    def insert_before_by_value(self, value: T, before_value: T) -> Union[BinaryTreeNode[T], None]:
        node_before = self.find_node_by_value(value=before_value)

        return self.insert_before(value=value, before_node=node_before)

    def insert_after(self, value: T, after_node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        if not after_node:
            return None

        new_node = BinaryTreeNode(value=value)

        if not after_node.right:
            after_node.right = new_node
        else:
            target_node = self.find_first_subtree_node(after_node.right)
            if target_node:
                target_node.left = new_node

        return new_node

    def insert_before(self, value: T, before_node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        if not before_node:
            return None

        new_node = BinaryTreeNode(value=value)

        if not before_node.left:
            before_node.left = new_node
        else:
            target_node = self.find_last_subtree_node(before_node.left)
            if target_node:
                target_node.right = new_node

        return new_node

    def delete_node_by_value(self, value: T) -> Union[BinaryTreeNode[T], None]:
        target_node = self.find_node_by_value(value=value)

        return self.delete_node(target_node)

    def delete_node(self, node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        if not node:
            return None

        parent_node = node.parent

        # Node is a leaf node
        if not node.left and not node.right:
            # Root node
            if not parent_node:
                self._root = None
            else:
                parent_node.delete_child(node)
        else:
            next_node: BinaryTreeNode[T] | None = None

            if node.left:
                next_node = self.find_predecessor(node)
            elif node.right:
                next_node = self.find_successor(node)

            if next_node:
                tmp_val = node.value
                node.value = next_node.value
                next_node.value = tmp_val
                return self.delete_node(next_node)

        return parent_node

    def export_to_image(self, filename: Union[str, None] = None):
        if not self._root:
            return

        queue = deque[BinaryTreeNode[T]]()
        queue.appendleft(self._root)
        graph = Graph(graph_attr=[("nodesep", "0.4"), ("ranksep", "0.5")])

        while len(queue) > 0:
            node = queue.popleft()

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

            graph.node(
                name=str(node.value),
                label=f"value={node.value}\nheight={node.height}\nsubtree_size={node.subtree_size}",
            )

            if node.parent:
                graph.edge(tail_name=str(node.parent.value), head_name=str(node.value))

        graph.render(
            filename=filename, format="png", directory="__generated__", view=True, overwrite_source=True, cleanup=True
        )

    def __len__(self) -> int:
        return self._root.subtree_size if self._root else 0


class RotatableOrderedBinaryTree(OrderedBinaryTree[T]):
    def __init__(self, root: Union[BinaryTreeNode[T], None] = None) -> None:
        super().__init__(root)
        self._root = root

    def rotate_right(self, node: BinaryTreeNode[T]) -> "RotatableOrderedBinaryTree[T]":
        if node.left:
            pivot = node.left

            if node.parent:
                if node.parent.left == node:
                    node.parent.left = pivot
                elif node.parent.right == node:
                    node.parent.right = pivot
            else:
                pivot.parent = None
                self._root = pivot

            if pivot.right:
                node.left = pivot.right
            else:
                node.left = None

            pivot.right = node

        return self

    def rotate_left(self, node: BinaryTreeNode[T]) -> "RotatableOrderedBinaryTree[T]":
        if node.right:
            pivot = node.right

            if node.parent:
                if node.parent.left == node:
                    node.parent.left = pivot
                elif node.parent.right == node:
                    node.parent.right = pivot
            else:
                pivot.parent = None
                self._root = pivot

            if pivot.left:
                node.right = pivot.left
            else:
                node.right = None

            pivot.left = node

        return self


class AVLTree(RotatableOrderedBinaryTree[T]):
    def __init__(self, root: Union[BinaryTreeNode[T], None] = None) -> None:
        super().__init__(root)
        self._root = root

    def insert_after(self, value: T, after_node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        new_node = super().insert_after(value, after_node)

        if new_node and new_node.parent:
            self._balance_subtree(node=new_node.parent)

        return new_node

    def insert_before(self, value: T, before_node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        new_node = super().insert_before(value, before_node)

        if new_node and new_node.parent:
            self._balance_subtree(node=new_node.parent)

        return new_node

    def delete_node(self, node: Union[BinaryTreeNode[T], None]) -> Union[BinaryTreeNode[T], None]:
        parent_node = super().delete_node(node)

        if parent_node:
            self._balance_subtree(node=parent_node)

        return parent_node

    def _get_node_balance_factor(self, node: BinaryTreeNode[T]):
        left_subtree_height = node.left.height + 1 if node.left else 0
        right_subtree_height = node.right.height + 1 if node.right else 0

        return right_subtree_height - left_subtree_height

    def _balance_subtree(self, node: BinaryTreeNode[T]):
        if not (node.left or node.right):
            return

        balance_factor = self._get_node_balance_factor(node=node)

        if balance_factor < -1:
            # Subtree is left-heavy - Rotating right
            if node.left and self._get_node_balance_factor(node=node.left) > 0:
                # Right child is right-heavy
                # - Rotating child to left
                self.rotate_left(node=node.left)

            self.rotate_right(node=node)
        elif balance_factor > 1:
            # Subtree is right-heavy - Rotating left
            if node.right and self._get_node_balance_factor(node=node.right) < 0:
                # Right child is left-heavy
                # - Rotating child to right
                self.rotate_right(node=node.right)

            self.rotate_left(node=node)

        if not node.parent:
            return

        return self._balance_subtree(node=node.parent)
