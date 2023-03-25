#!/usr/bin/env python3

from typing import Generic, TypeVar, Union
from .linked_list import DoublyLinkedList

T = TypeVar("T")


class ArrayQueue(Generic[T]):
    def __init__(self) -> None:
        self._queue: list[T] = []

    def is_empty(self) -> int:
        return len(self._queue) == 0

    def enqueue(self, item: T) -> None:
        return self._queue.append(item)

    def dequeue(self) -> Union[T, None]:
        item = self.peek()

        if not self.is_empty():
            self._queue = self._queue[1 : len(self._queue)]

        return item

    def peek(self) -> Union[T, None]:
        if not self.is_empty():
            return self._queue[0]

    def __repr__(self) -> str:
        return str(self._queue)

    def __len__(self) -> int:
        return len(self._queue)


class ListQueue(Generic[T]):
    def __init__(self) -> None:
        self._queue = DoublyLinkedList[T]()

    def enqueue(self, item: T) -> None:
        self._queue.append(item)

    def peek(self) -> Union[T, None]:
        return self._queue.head

    def dequeue(self) -> Union[T, None]:
        item = self.peek()

        self._queue.remove_head()

        return item

    def is_empty(self) -> bool:
        return self._queue.size == 0

    def __repr__(self) -> str:
        return str(self._queue.to_array())

    def __len__(self) -> int:
        return self._queue.size


class CircularBufferQueue(Generic[T]):
    def __init__(self, capacity: int, allow_overwrite=False) -> None:
        self._capacity = capacity
        self._allow_overwrite = allow_overwrite
        self._read_pointer = 0
        self._write_pointer = 0
        self._size = 0
        self._queue: list[T | None] = [None] * (capacity)

    def enqueue(self, item: T) -> None:
        if self._queue[self._write_pointer] is not None and not self._allow_overwrite:
            raise ValueError("Buffer is full")

        self._queue[self._write_pointer] = item

        if self._read_pointer == self._write_pointer and self._size > 0:
            self._read_pointer += 1
            if self._read_pointer >= self._capacity:
                self._read_pointer = 0

        self._write_pointer = (self._write_pointer + 1) % self._capacity

        if self._size < self._capacity:
            self._size += 1

    def dequeue(self) -> Union[T, None]:
        item = self._queue[self._read_pointer]
        self._queue[self._read_pointer] = None

        if self._size > 0:
            self._read_pointer = (self._read_pointer + 1) % self._capacity
            self._size -= 1

        return item

    def peek(self) -> Union[T, None]:
        return self._queue[self._read_pointer]

    def is_empty(self) -> bool:
        return self._size == 0

    def __repr__(self) -> str:
        return str(self._queue)

    def __len__(self) -> int:
        return self._size


queue = ArrayQueue[int]()
print(queue.is_empty())
queue.enqueue(1)
queue.enqueue(2)
print(queue, len(queue), queue.is_empty())
print(queue.peek())
print(queue.dequeue())
print(queue)
print(queue.dequeue())
print(queue.is_empty())
print(queue)
print(queue.dequeue())
queue.enqueue(1)
print(queue.dequeue())
print(queue)
print("\n\n")

list_queue = ListQueue[int]()
print(list_queue.is_empty())
list_queue.enqueue(1)
list_queue.enqueue(2)
print(list_queue, len(list_queue), list_queue.is_empty())
print(list_queue.peek())
print(list_queue.dequeue())
print(list_queue)
print(list_queue.dequeue())
print(list_queue.is_empty())
print(list_queue)
print(list_queue.dequeue())
list_queue.enqueue(1)
print(list_queue.dequeue())
print(list_queue)
print("\n\n")

circular_buffer_queue = CircularBufferQueue[int](3, allow_overwrite=True)
print(circular_buffer_queue.is_empty())
circular_buffer_queue.enqueue(1)
circular_buffer_queue.enqueue(2)
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
print(circular_buffer_queue.peek())
print(circular_buffer_queue.dequeue())
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
print(circular_buffer_queue.dequeue())
print(circular_buffer_queue.is_empty())
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
print(circular_buffer_queue.dequeue())
circular_buffer_queue.enqueue(1)
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
print(circular_buffer_queue.dequeue())
print(circular_buffer_queue.dequeue())
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
circular_buffer_queue.enqueue(1)
circular_buffer_queue.enqueue(2)
circular_buffer_queue.enqueue(3)

print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
circular_buffer_queue.enqueue(4)
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
print(circular_buffer_queue.dequeue())
print(circular_buffer_queue.dequeue())
print(circular_buffer_queue.dequeue())
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
circular_buffer_queue.dequeue()
print(
    circular_buffer_queue,
    len(circular_buffer_queue),
    circular_buffer_queue.is_empty(),
    circular_buffer_queue._read_pointer,
    circular_buffer_queue._write_pointer,
)
