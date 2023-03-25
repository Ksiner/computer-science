from typing import Generic, TypeVar

T = TypeVar("T", int, str)


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._stack: list[T] = []

    def push(self, item: T) -> None:
        self._stack.append(item)

    def peek(self) -> T:
        return self._stack[len(self._stack) - 1]

    def pop(self) -> T:
        item = self.peek()
        self._stack = self._stack[0 : len(self._stack) - 1]

        return item

    def is_empty(self):
        return len(self._stack) == 0

    def __repr__(self) -> str:
        return str(self._stack)

    def __len__(self) -> int:
        return len(self._stack)


stack = Stack[int]()
stack.push(1)
stack.push(2)
stack.push(3)
print("len(stack)", len(stack))
print(stack)
print(stack.peek())
print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
print("len(stack)", len(stack))
