from typing import Generic, TypeVar, Union, Callable, cast
from .linked_list import DoublyLinkedList, Node

K = TypeVar("K")
V = TypeVar("V")


class HashTable(Generic[K, V]):
    def __init__(self) -> None:
        self._hash: dict[K, V] = {}

    def add(self, key: K, item: V) -> "HashTable[K, V]":
        self._hash[key] = item

        return self

    def add_items(self, items: dict[K, V]) -> "HashTable[K, V]":
        for key, value in items.items():
            self.add(key, value)

        return self

    def get(self, key: K) -> Union[V, None]:
        return self._hash[key]

    def delete(self, key: K) -> "HashTable[K, V]":
        self._hash.pop(key)

        return self

    def size(self) -> int:
        return len(self._hash.keys())

    def __len__(self) -> int:
        return self.size()

    def clear(self) -> "HashTable[K, V]":
        self._hash = {}

        return self


class HashTableWithRealHashesAndCollisions(Generic[V]):
    _predefined_collision_keys_map = {"1": "1", "2": "1", "3": "1"}

    def __init__(self) -> None:
        self._size = 0
        self._hash: dict[str, dict[str, V]] = {}

    def add(self, key: str, item: V) -> "HashTableWithRealHashesAndCollisions[V]":
        collision_key = self._predefined_collision_keys_map.get(key)
        target_key = collision_key or key

        existing_value_by_key = self._hash.get(target_key)

        if existing_value_by_key:
            if not existing_value_by_key.get(key):
                self._size += 1

            existing_value_by_key[key] = item
        else:
            self._hash[target_key] = {key: item}
            self._size += 1

        return self

    def add_items(self, items: dict[str, V]) -> "HashTableWithRealHashesAndCollisions[V]":
        for key, value in items.items():
            self.add(key, value)

        return self

    def get(self, key: str) -> Union[V, None]:
        collision_key = self._predefined_collision_keys_map[key]
        item = self._hash[collision_key or key][key]

        return item

    def delete(self, key: str) -> "HashTableWithRealHashesAndCollisions[V]":
        collision_key = self._predefined_collision_keys_map[key]
        target_key = collision_key or key
        item = self._hash.get(target_key)

        if item:
            item.pop(key)
            if len(item) == 0:
                self._hash.pop(target_key)

        return self

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self.size()

    def clear(self) -> "HashTableWithRealHashesAndCollisions[V]":
        self._hash = {}

        return self


hash_table = HashTable[str, int]()
hash_table.add("1", 1).add_items({"2": 2, "3": 3})
print(hash_table.get("3"), hash_table.get("2"))
print(len(hash_table), hash_table.size())
print(hash_table.clear().size(), hash_table.get("3"))

hash_table = HashTableWithRealHashesAndCollisions[int]()
hash_table.add("1", 1).add_items({"2": 2, "3": 3})
print(hash_table.get("3"), hash_table.get("2"))
print(len(hash_table), hash_table.size())
print(hash_table.clear().size(), hash_table.get("3"))


def division_hash(prehash: int, divider: int) -> int:
    return prehash % divider


class ChainingHashTableListValue(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value


class ChainingHashTable(Generic[K, V]):
    def __init__(self, auto_grow: bool = False, hash_func: Callable[[K, int], int] = division_hash) -> None:
        self._auto_grow = auto_grow
        self._hash_func = hash_func
        self._capacity = 2**2
        self._capacity_modification_factor = 2**1
        self._shrink_ratio = 1 / 4
        self._size = 0
        self._hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None] = [None] * self._capacity

    def _add(
        self,
        hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None],
        index: int,
        item: ChainingHashTableListValue[K, V],
    ) -> None:
        """Private generic utility function to properly add item to a provided hash table"""
        if hash_table[index]:
            cast(DoublyLinkedList[ChainingHashTableListValue[K, V]], hash_table[index]).append(value=item)
        else:
            hash_table[index] = DoublyLinkedList[ChainingHashTableListValue[K, V]]().append(value=item)

    def _rehash(
        self,
        old_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None],
        new_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None],
    ):
        for items_list in old_table:
            if items_list:
                for item in items_list:
                    new_item_hash = self._hash_func(item.value.key, len(new_table) - 1)
                    self._add(hash_table=new_table, index=new_item_hash, item=item.value)

    def _grow(self) -> None:
        """Table Doubling"""
        new_capacity = self._capacity * self._capacity_modification_factor
        new_hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None] = [None] * new_capacity

        self._rehash(old_table=self._hash_table, new_table=new_hash_table)

        self._capacity = new_capacity
        self._hash_table = new_hash_table

    def _shrink(self) -> None:
        new_capacity = int(self._capacity / self._capacity_modification_factor)
        new_hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]] | None] = [None] * new_capacity

    def _should_grow(self) -> bool:
        if self._size == 0:
            return False

        return self._size / self._capacity == 1

    def _should_shrink(self) -> bool:
        if self._size == 0:
            return False

        return self._size / self._capacity <= self._shrink_ratio

    def add(self, key: K, value: V) -> "ChainingHashTable[K, V]":
        hashed_key = self._hash_func(key, self._capacity)
        new_item = ChainingHashTableListValue[K, V](key, value)

        self._add(hash_table=self._hash_table, index=hashed_key, item=new_item)
        self._size += 1

        if self._auto_grow and self._should_grow():
            self._grow()

        return self

    def search(self, key: K) -> V:
        item = self._hash_table[self._hash_func(key, self._capacity)]

        if item:
            item.search()
