from typing import Union
from .linked_list import DoublyLinkedList, Node
from .hash_table import ChainingHashTable
from .trees.binary_tree import OrderedBinaryTree, BinaryTreeNode
from unittest import TestCase as UnitTestCase


class TestBase:
    def run(self) -> None:
        raise NotImplementedError()


class TestCase:
    def __init__(self, name: str, tests_or_sub_cases: Union[list[Union[TestBase, "TestCase"]], None] = None) -> None:
        self._name = name
        self._tests_or_sub_cases = tests_or_sub_cases or []

    def run(self, depth: int = 0):
        print(("\t" * depth) + self._name)

        for test_or_case in self._tests_or_sub_cases:
            if isinstance(test_or_case, TestBase):
                print(("\t" * (depth + 1)) + test_or_case.__class__.__name__)

                test_or_case.run()

                print(("\t" * (depth + 2)) + "passed ✅")
            else:
                test_or_case.run(depth=depth + 1)

        print(("\t" * (depth)) + "passed ✅")


class LinkedListTest1(TestBase):
    def run(self) -> None:
        node1 = Node(1)
        node2 = Node(2)
        test_list_1 = DoublyLinkedList(node1)
        test_list_1.append_by_node(node2)
        assert test_list_1.to_array_of_nodes() == [node1, node2]
        assert test_list_1.to_array() == [node1.value, node2.value]

        test_list_1.remove_head()
        assert test_list_1.to_array_of_nodes() == [node2]
        assert test_list_1.to_array() == [node2.value]

        test_list_1.remove_tail()
        assert test_list_1.to_array_of_nodes() == []
        assert test_list_1.to_array() == []

        node4 = Node(4)
        node5 = Node(5)
        node3 = Node(3)
        node2 = Node(2)
        test_list_1.append_by_node(node4)
        test_list_1.append_by_node(node5)
        test_list_1.prepend_by_node(node3)
        test_list_1.prepend_by_node(node2)
        assert test_list_1.to_array_of_nodes() == [node2, node3, node4, node5]
        assert test_list_1.to_array() == [node2.value, node3.value, node4.value, node5.value]

        test_list_1.remove_tail()
        assert test_list_1.search(value=5) == None

        test_list_1.remove_head()
        assert test_list_1.search(value=2) == None


class LinkedListTest2(TestBase):
    def run(self) -> None:
        test_list_2 = DoublyLinkedList()
        assert test_list_2.to_array_of_nodes() == []
        assert test_list_2.head == None
        assert test_list_2.tail == None
        assert (test_list_2.head == test_list_2.tail) == True

        node1 = Node(1)
        node2 = Node(2)
        test_list_2.append_by_node(node1)
        assert test_list_2.to_array_of_nodes() == [node1]
        assert test_list_2.to_array() == [node1.value]

        test_list_2.append_by_node(node2)
        assert test_list_2.to_array_of_nodes() == [node1, node2]
        assert test_list_2.to_array() == [node1.value, node2.value]

        test_list_2.remove_head()
        assert test_list_2.to_array_of_nodes() == [node2]
        assert test_list_2.to_array() == [node2.value]

        test_list_2.remove_head()
        assert test_list_2.to_array_of_nodes() == []
        assert test_list_2.to_array() == []

        test_list_2.prepend_by_node(node1)
        assert test_list_2.to_array_of_nodes() == [node1]
        assert test_list_2.to_array() == [node1.value]

        test_list_2.prepend_by_node(node2)
        assert test_list_2.to_array_of_nodes() == [node2, node1]
        assert test_list_2.to_array() == [node2.value, node1.value]

        test_list_2.remove_tail()
        assert test_list_2.to_array_of_nodes() == [node2]
        assert test_list_2.to_array() == [node2.value]

        test_list_2.remove_tail()
        assert test_list_2.to_array_of_nodes() == []
        assert test_list_2.to_array() == []


class ChainingHashTableWithoutTableDoublingTest(TestBase):
    def run(self) -> None:
        hash_table = ChainingHashTable[int, int]()
        hash_table.add(key=1, value=1)
        hash_table.add(2, 1)
        hash_table.add(3, 1)
        hash_table.add(4, 1)
        hash_table.add(5, 1)
        assert len(hash_table) == 5

        has_collisions = False

        for list_item in hash_table._hash_table:
            if len(list_item) > 1:
                has_collisions = True

        assert has_collisions == True

        assert hash_table.get(5) == 1
        assert hash_table.add(5, 2).get(5) == 2

        hash_table.delete(5)
        assert len(hash_table) == 4
        assert hash_table.get(5) is None
        assert hash_table.get(6) is None

        hash_table.delete(6)
        assert len(hash_table) == 4


class ChainingHashTableWithTableDoublingTest(TestBase):
    def run(self) -> None:
        hash_table = ChainingHashTable[str, int](auto_size=True)
        [key1, key2, key3, key4, key5] = ["PNGHPqYORV", "ogICwMlVqX", "UMiMidgRYu", "3xUbcEz6Lv", "lwDqElbH2g"]
        hash_table.add(key=key1, value=1)
        hash_table.add(key2, 2)
        hash_table.add(key3, 3)
        assert hash_table._capacity == 4
        hash_table.add(key4, 4)

        assert hash_table._capacity == 8

        hash_table.add(key5, 5)

        assert hash_table._capacity == 8

        assert len(hash_table) == 5

        assert hash_table.get(key5) == 5
        assert hash_table.add(key5, 6).get(key5) == 6

        hash_table.delete(key5)

        assert len(hash_table) == 4
        assert hash_table.get(key5) is None
        assert hash_table._capacity == 8

        hash_table.delete(key4)

        assert hash_table._capacity == 8

        hash_table.delete(key3)

        assert len(hash_table) == 2
        assert hash_table._capacity == 4


class SingleNodeOrderedBinaryTreeTest(TestBase):
    def run(self) -> None:
        # Tree Itself
        binary_tree = OrderedBinaryTree()

        assert binary_tree.height == 0
        assert len(binary_tree) == 0

        # Tree Root
        root = BinaryTreeNode(value=1)

        binary_tree.root = root

        assert binary_tree.height == 0
        assert len(binary_tree) == 1

        node_unknown = binary_tree.find_node_by_value(7)
        node_unknown_successor = binary_tree.find_successor_by_value(7)

        assert not node_unknown
        assert not node_unknown_successor


class MultipleNodesOrderedBinaryTreeTest(TestBase):
    def run(self) -> None:
        # Tree Structure
        root = BinaryTreeNode(
            value=2,
            left=BinaryTreeNode(
                value=4,
                left=BinaryTreeNode(value=5, left=BinaryTreeNode(value=6)),
                right=BinaryTreeNode(value=3, right=BinaryTreeNode(value=2.5)),
            ),
            right=BinaryTreeNode(value=1),
        )

        # Tree Itself
        binary_tree = OrderedBinaryTree(root=root)

        assert binary_tree.height == 3
        assert len(binary_tree) == 7
        assert root.left and root.left.parent == root
        assert root.right and root.right.parent == root

        node_6 = binary_tree.find_node_by_value(6)
        node_6_successor = binary_tree.find_successor_by_value(6)

        assert node_6 and node_6.value == 6
        assert node_6_successor and node_6_successor.value == 5

        node_2_5 = binary_tree.find_node_by_value(2.5)
        node_2_5_successor = binary_tree.find_successor_by_value(2.5)

        assert node_2_5 and node_2_5.value == 2.5
        assert node_2_5_successor and node_2_5_successor.value == 2

        node_unknown = binary_tree.find_node_by_value(7)
        node_unknown_successor = binary_tree.find_successor_by_value(7)

        assert not node_unknown
        assert not node_unknown_successor

        root_node = binary_tree.find_node_by_value(2)
        root_node_successor = binary_tree.find_successor_by_value(2)

        assert root_node and root_node == root
        assert root_node_successor and root_node_successor.value == 1


class RightOnlyNodesOrderedBinaryTreeTest(TestBase):
    def run(self) -> None:
        # Tree Structure
        root = BinaryTreeNode(
            value=1,
            right=BinaryTreeNode(value=2, right=BinaryTreeNode(value=3, right=BinaryTreeNode(value=4))),
        )
        binary_tree = OrderedBinaryTree(root=root)

        assert binary_tree.height == 3
        assert len(binary_tree) == 4

        node_3_successor = binary_tree.find_successor_by_value(3)

        assert node_3_successor and node_3_successor.value == 4

        node_4_successor = binary_tree.find_successor_by_value(4)

        assert not node_4_successor


class PredecessorSearchOnOrderedBinaryTreeTest(TestBase):
    def run(self) -> None:
        # Tree Structure -- Right Only
        right_only_root = BinaryTreeNode(
            value=1,
            right=BinaryTreeNode(value=2, right=BinaryTreeNode(value=3, right=BinaryTreeNode(value=4))),
        )
        right_only_binary_tree = OrderedBinaryTree(root=right_only_root)

        node_3_predecessor = right_only_binary_tree.find_predecessor_by_value(3)

        assert node_3_predecessor and node_3_predecessor.value == 2

        root_predecessor = right_only_binary_tree.find_predecessor_by_value(1)

        assert not root_predecessor

        # Tree Structure -- Left Only Tree
        left_only_root = BinaryTreeNode(value=3, left=BinaryTreeNode(value=2, left=BinaryTreeNode(value=1)))
        left_only_binary_tree = OrderedBinaryTree(root=left_only_root)

        node_1_predecessor = left_only_binary_tree.find_predecessor_by_value(1)

        assert not node_1_predecessor

        root_predecessor = left_only_binary_tree.find_predecessor_by_value(3)

        assert root_predecessor and root_predecessor.value == 2

        # Tree Structure -- Mixed Tree
        mixed_tree_root = BinaryTreeNode(
            value=2,
            left=BinaryTreeNode(
                value=5,
                left=BinaryTreeNode(value=6, left=BinaryTreeNode(value=7)),
                right=BinaryTreeNode(value=4, right=BinaryTreeNode(value=3)),
            ),
            right=BinaryTreeNode(value=1),
        )
        mixed_binary_tree = OrderedBinaryTree(root=mixed_tree_root)

        root_predecessor = mixed_binary_tree.find_predecessor_by_value(2)

        assert root_predecessor and root_predecessor.value == 3


TestCase(
    "Tests",
    tests_or_sub_cases=[
        TestCase("Linked List Tests", tests_or_sub_cases=[LinkedListTest1(), LinkedListTest2()]),
        TestCase(
            name="Hash Tables",
            tests_or_sub_cases=[
                TestCase(
                    name="Chaining",
                    tests_or_sub_cases=[
                        ChainingHashTableWithoutTableDoublingTest(),
                        ChainingHashTableWithTableDoublingTest(),
                    ],
                )
            ],
        ),
        TestCase(
            name="Trees",
            tests_or_sub_cases=[
                TestCase(
                    name="Binary Tree",
                    tests_or_sub_cases=[
                        TestCase(
                            name="Ordered Binary Tree",
                            tests_or_sub_cases=[
                                SingleNodeOrderedBinaryTreeTest(),
                                MultipleNodesOrderedBinaryTreeTest(),
                                RightOnlyNodesOrderedBinaryTreeTest(),
                                PredecessorSearchOnOrderedBinaryTreeTest(),
                            ],
                        )
                    ],
                )
            ],
        ),
    ],
).run()


class InsertAfterOnOrderedBinaryTreeTest(UnitTestCase):
    def test_right_only_list(self) -> None:
        # Tree Structure -- Right Only
        right_only_root = BinaryTreeNode[float](
            value=1,
            right=BinaryTreeNode(value=2, right=BinaryTreeNode(value=3, right=BinaryTreeNode(value=4))),
        )
        right_only_binary_tree = OrderedBinaryTree(root=right_only_root)

        right_only_binary_tree.insert_after_by_value(value=7, after_value=8)

        self.assertEqual(len(right_only_binary_tree), 4)
        self.assertEqual(right_only_binary_tree.height, 3)

        right_only_binary_tree.insert_after_by_value(value=5, after_value=4)

        self.assertEqual(len(right_only_binary_tree), 5)
        self.assertEqual(right_only_binary_tree.height, 4)
        self.assertListEqual([node.value for node in right_only_binary_tree.traverse_tree()], [1, 2, 3, 4, 5])

        node_4 = right_only_binary_tree.find_node_by_value(4)

        self.assertIsNotNone(node_4)
        self.assertIsNotNone(node_4.right if node_4 else node_4)
        self.assertIsNotNone(node_4.right.value if node_4 and node_4.right else node_4, 5)

        right_only_binary_tree.insert_after_by_value(value=4.5, after_value=4)

        self.assertEqual(len(right_only_binary_tree), 6)
        self.assertEqual(right_only_binary_tree.height, 5)
        self.assertListEqual([node.value for node in right_only_binary_tree.traverse_tree()], [1, 2, 3, 4, 4.5, 5])

        node_5 = right_only_binary_tree.find_node_by_value(5)

        self.assertIsNotNone(node_5)
        self.assertIsNotNone(node_5.left if node_5 else None)
        self.assertEqual(node_5.left.value if node_5 and node_5.left else None, 4.5)

    def test_left_only_list(self) -> None:
        # Tree Structure -- Left Only
        left_only_root = BinaryTreeNode[float](value=3, left=BinaryTreeNode(value=2, left=BinaryTreeNode(value=1)))
        left_only_binary_tree = OrderedBinaryTree(root=left_only_root)

        left_only_binary_tree.insert_after_by_value(value=7, after_value=8)

        self.assertEqual(len(left_only_binary_tree), 3)
        self.assertEqual(left_only_binary_tree.height, 2)

        left_only_binary_tree.insert_after_by_value(value=1.5, after_value=1)

        self.assertEqual(len(left_only_binary_tree), 4)
        self.assertEqual(left_only_binary_tree.height, 3)
        self.assertListEqual([node.value for node in left_only_binary_tree.traverse_tree()], [1, 1.5, 2, 3])

        node_1 = left_only_binary_tree.find_node_by_value(1)

        self.assertIsNotNone(node_1)
        self.assertIsNotNone(node_1.right if node_1 else node_1)
        self.assertEqual(node_1.right.value if node_1 and node_1.right else node_1, 1.5)

        left_only_binary_tree.insert_after_by_value(value=4, after_value=3)

        self.assertEqual(len(left_only_binary_tree), 5)
        self.assertEqual(left_only_binary_tree.height, 3)
        self.assertListEqual([node.value for node in left_only_binary_tree.traverse_tree()], [1, 1.5, 2, 3, 4])

        node_3 = left_only_binary_tree.find_node_by_value(3)

        self.assertIsNotNone(node_3)
        self.assertIsNotNone(node_3.right if node_3 else node_3)
        self.assertEqual(node_3.right.value if node_3 and node_3.right else node_3, 4)


class DeleteNodeOnOrderedBinaryTreeTest(UnitTestCase):
    def test_right_only_list(self) -> None:
        # Tree Structure -- Right Only
        right_only_root = BinaryTreeNode[float](
            value=1,
            right=BinaryTreeNode(value=2, right=BinaryTreeNode(value=3, right=BinaryTreeNode(value=4))),
        )
        right_only_binary_tree = OrderedBinaryTree(root=right_only_root)

        # Deleting non-existing node
        right_only_binary_tree.delete_node_by_value(value=5)

        self.assertEqual(len(right_only_binary_tree), 4)
        self.assertEqual(right_only_binary_tree.height, 3)

        # Deleting root node (which is also the first node in case of InOrder traversal)
        right_only_binary_tree.delete_node_by_value(1)

        self.assertEqual(len(right_only_binary_tree), 3)
        self.assertEqual(right_only_binary_tree.height, 2)
        self.assertEqual(right_only_binary_tree.root.value if right_only_binary_tree.root else None, 2)
        self.assertListEqual([node.value for node in right_only_binary_tree.traverse_tree()], [2, 3, 4])

        # Deleting the last/leaf node
        right_only_binary_tree.delete_node_by_value(4)

        self.assertEqual(len(right_only_binary_tree), 2)
        self.assertEqual(right_only_binary_tree.height, 1)
        self.assertEqual(right_only_binary_tree.root.value if right_only_binary_tree.root else None, 2)
        self.assertListEqual([node.value for node in right_only_binary_tree.traverse_tree()], [2, 3])

        # Deleting all the nodes of the tree
        right_only_binary_tree.delete_node_by_value(2).delete_node_by_value(3)

        self.assertEqual(len(right_only_binary_tree), 0)
        self.assertEqual(right_only_binary_tree.height, 0)
        self.assertIsNone(right_only_binary_tree.root)
        self.assertListEqual([node.value for node in right_only_binary_tree.traverse_tree()], [])

    def test_left_only_list(self) -> None:
        # Tree Structure -- Left Only
        left_only_root = BinaryTreeNode[float](value=3, left=BinaryTreeNode(value=2, left=BinaryTreeNode(value=1)))
        left_only_binary_tree = OrderedBinaryTree(root=left_only_root)

        # Deleting the root node (which is also the last node in case of In-Order traversal)
        left_only_binary_tree.delete_node_by_value(value=3)

        self.assertEqual(len(left_only_binary_tree), 2)
        self.assertEqual(left_only_binary_tree.height, 1)
        self.assertEqual(left_only_binary_tree.root.value if left_only_binary_tree.root else None, 2)
        self.assertListEqual([node.value for node in left_only_binary_tree.traverse_tree()], [1, 2])

    def test_mixed_tree(self) -> None:
        mixed_root = BinaryTreeNode(
            value=4, left=BinaryTreeNode(value=2, left=BinaryTreeNode(value=1), right=BinaryTreeNode(value=3))
        )
        mixed_binary_tree = OrderedBinaryTree(root=mixed_root)

        mixed_binary_tree.delete_node_by_value(4)

        self.assertEqual(len(mixed_binary_tree), 3)
        self.assertEqual(mixed_binary_tree.height, 2)
        self.assertEqual(mixed_binary_tree.root.value if mixed_binary_tree.root else None, 3)
        self.assertListEqual([node.value for node in mixed_binary_tree.traverse_tree()], [1, 2, 3])
