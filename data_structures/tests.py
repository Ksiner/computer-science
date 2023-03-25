from typing import Union
from .linked_list import DoublyLinkedList, Node
from .hash_table import ChainingHashTable


class AbstractTest:
    def run(self) -> None:
        raise NotImplementedError()


class TestCase:
    def __init__(
        self, name: str, tests_or_sub_cases: Union[list[Union[AbstractTest, "TestCase"]], None] = None
    ) -> None:
        self._name = name
        self._tests_or_sub_cases = tests_or_sub_cases or []

    def run(self, depth: int = 0):
        print(("\t" * depth) + self._name)

        for test_or_case in self._tests_or_sub_cases:
            if isinstance(test_or_case, AbstractTest):
                print(("\t" * (depth + 1)) + test_or_case.__class__.__name__)

                test_or_case.run()

                print(("\t" * (depth + 2)) + "passed ✅")
            else:
                test_or_case.run(depth=depth + 1)

        print(("\t" * (depth)) + "passed ✅")


class LinkedListTest1(AbstractTest):
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


class LinkedListTest2(AbstractTest):
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


class ChainingHashTableWithoutTableDoublingTest(AbstractTest):
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


class ChainingHashTableWithTableDoublingTest(AbstractTest):
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
    ],
).run()
