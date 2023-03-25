from .linked_list import DoublyLinkedList, Node

# Linked List
print("Linked List tests:")
print("\tcase 1: Test List 1")
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
assert test_list_1.search_by_value(5) == None
test_list_1.remove_head()
assert test_list_1.search_by_value(2) == None
print("\t\tpassed ✅")

print("\tcase 2: Test List 2")
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
print("\t\tpassed ✅\n")
