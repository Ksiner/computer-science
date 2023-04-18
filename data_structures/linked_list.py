#!/usr/bin/env python3

from typing import Union, TypeVar, Generic, Callable

T = TypeVar("T")


class Node(Generic[T]):
    @property
    def value(self) -> T:
        return self.__value

    @value.setter
    def value(self, newValue: T) -> None:
        self.__value = newValue

    def __init__(self, value: T, next: Union["Node[T]", None] = None, prev: Union["Node[T]", None] = None):
        self.value = value
        self.next = next
        self.prev = prev

    def __repr__(self) -> str:
        return str(self.value)


class DoublyLinkedList(Generic[T]):
    @property
    def size(self) -> int:
        return self._size

    @property
    def head_node(self) -> Union[Node[T], None]:
        return self._head

    @property
    def head(self) -> Union[T, None]:
        if self._head:
            return self._head.value

    @property
    def tail_node(self) -> Union[Node[T], None]:
        return self._tail

    @property
    def tail(self) -> Union[T, None]:
        if self._tail:
            return self._tail.value

    def __init__(self, node: Union[Node[T], None] = None):
        if node is not None:
            node.next = None
            node.prev = None
            self._size = 1
        else:
            self._size = 0

        self._head = node
        self._tail = node

    def prepend_by_node(self, node: Node[T]) -> "DoublyLinkedList[T]":
        # cases to handle:
        # empty list
        # any number of elements on the list (1..N)

        if self._head:
            # empty list case
            self._head.prev = node
        else:
            self._tail = node

        node.prev = None
        node.next = self._head
        self._head = node
        self._size += 1

        return self

    def prepend(self, value: T) -> "DoublyLinkedList[T]":
        # cases to handle:
        # empty list
        # any number of elements on the list (1..N)

        return self.prepend_by_node(Node(value))

    def append_by_node(self, node: Node[T]) -> "DoublyLinkedList[T]":
        # cases to handle:
        # empty list
        # any number of elements on the list (1..N)

        if self._tail:
            # empty list case
            self._tail.next = node
        else:
            self._head = node

        node.prev = self._tail
        node.next = None
        self._tail = node
        self._size += 1

        return self

    def append(self, value: T) -> "DoublyLinkedList[T]":
        # cases to handle:
        # empty list
        # any number of elements on the list (1..N)
        return self.append_by_node(Node(value))

    def remove_head(self):
        if self._head is None:
            return self

        self.remove_node(self._head)

        return self

    def remove_tail(self):
        if self._tail is None:
            return self

        self.remove_node(self._tail)

        return self

    def remove_node(self, node: Node[T]):
        # cases to handle:
        # header node encountered
        # tail node encountered
        # single node encountered
        # simple node encountered

        if node.prev and node.next:
            node.prev.next = node.next
            node.next.prev = node.prev
        else:
            if node.prev is None:
                # header node encountered
                # setting new head node
                if node.next:
                    node.next.prev = None
                self._head = node.next

            if node.next is None:
                # tail node encountered
                # setting tail node
                if node.prev:
                    node.prev.next = None
                self._tail = node.prev

            # single node case handled by 2 'if' bocks above
        self._size -= 1

        return self

    def remove_node_by_value(self, value: T):
        target_node = self.search_node(value=value)

        if not target_node:
            return self

        return self.remove_node(node=target_node)

    def search_node(
        self, search_func: Union[Callable[[T], bool], None] = None, value: Union[T, None] = None
    ) -> Union[Node[T], None]:
        current_node = self._head

        while current_node is not None:
            if (search_func and search_func(current_node.value)) or (current_node.value == value):
                return current_node

            current_node = current_node.next

        return None

    def search(
        self, search_func: Union[Callable[[T], bool], None] = None, value: Union[T, None] = None
    ) -> Union[T, None]:
        target_node = self.search_node(search_func=search_func, value=value)

        if target_node:
            return target_node.value

        return None

    def to_array_of_nodes(self) -> list[Node[T]]:
        arr: list[Node[T]] = []
        current_node = self._head

        while current_node is not None:
            arr.append(current_node)
            current_node = current_node.next

        return arr

    def to_array(self) -> list[T]:
        arr: list[T] = []
        current_node = self._head

        while current_node is not None:
            arr.append(current_node.value)
            current_node = current_node.next

        return arr

    def print(self) -> None:
        if self._head is None:
            return print("The list is empty")

        curr_el = self._head

        while curr_el:
            print(
                f"List el '{curr_el}';\n\tPrev el: '{curr_el.prev if curr_el and curr_el.prev else 'None'}';\n\tNext el: '{curr_el.next if curr_el and curr_el.next else 'None'}'"
            )
            curr_el = curr_el.next

    def __iter__(self):
        self._iter_pointer = self._head

        return self

    def __next__(self) -> Node[T]:
        if self._iter_pointer:
            current_item = self._iter_pointer
            self._iter_pointer = self._iter_pointer.next

            return current_item
        else:
            raise StopIteration

    def __len__(self) -> int:
        return self._size
