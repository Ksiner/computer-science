from typing import Generic, TypeVar, Union, Callable, cast, Any
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


def division_hash(key: Any, divider: int) -> int:
    return hash(key) % divider


class ChainingHashTableListValue(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value


class ChainingHashTable(Generic[K, V]):
    def __init__(self, auto_size: bool = False, hash_func: Callable[[K, int], int] = division_hash) -> None:
        self._auto_size = auto_size
        self._hash_func = hash_func
        self._capacity = 2**2
        self._capacity_modification_factor = 2**1
        self._shrink_ratio = 1 / 4
        self._size = 0
        self._hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]]] = self._init_new_list(self._capacity)

    def _init_new_list(self, length: int) -> list[DoublyLinkedList[ChainingHashTableListValue[K, V]]]:
        return [DoublyLinkedList[ChainingHashTableListValue[K, V]]() for _ in range(length)]

    def _add_or_update(
        self,
        hash_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]]],
        index: int,
        item: ChainingHashTableListValue[K, V],
    ) -> bool:
        """Private generic utility function to properly add item to a provided hash table"""
        existing_item = hash_table[index].search(search_func=self._get_list_search_func(key=item.key))

        if existing_item:
            existing_item.value = item.value
            return False
        else:
            hash_table[index].append(value=item)
            return True

    def _rehash(
        self,
        old_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]]],
        new_table: list[DoublyLinkedList[ChainingHashTableListValue[K, V]]],
    ):
        """Method that rehashes the values from old_table to a new_table"""
        for items_list in old_table:
            for item in items_list:
                new_item_hash = self._hash_func(item.value.key, len(new_table))
                self._add_or_update(hash_table=new_table, index=new_item_hash, item=item.value)

    def _change_hash_table_size(self, new_capacity: int) -> None:
        """Method that actually structures new hash table with updated capacity"""
        new_hash_table = self._init_new_list(new_capacity)

        self._rehash(old_table=self._hash_table, new_table=new_hash_table)

        self._capacity = new_capacity
        self._hash_table = new_hash_table

    def _grow(self) -> None:
        """Table Doubling Grow"""
        self._change_hash_table_size(self._capacity * self._capacity_modification_factor)

    def _shrink(self) -> None:
        """Table Doubling Shrink"""
        self._change_hash_table_size(int(self._capacity / self._capacity_modification_factor))

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

        item_added = self._add_or_update(hash_table=self._hash_table, index=hashed_key, item=new_item)

        if item_added:
            self._size += 1

        if self._auto_size and self._should_grow():
            self._grow()

        return self

    def _get_list_search_func(self, key: K) -> Callable[[ChainingHashTableListValue[K, V]], bool]:
        return lambda list_item: list_item.key == key

    def get(self, key: K) -> Union[V, None]:
        item = self._hash_table[self._hash_func(key, self._capacity)].search(
            search_func=self._get_list_search_func(key)
        )

        if not item:
            return None

        return item.value

    def delete(self, key: K) -> Union[V, None]:
        target_list = self._hash_table[self._hash_func(key, self._capacity)]
        list_node = target_list.search_node(search_func=self._get_list_search_func(key))
        if not list_node:
            return None

        target_list.remove_node(list_node)
        self._size -= 1

        if self._auto_size and self._should_shrink():
            self._shrink()

        return list_node.value.value

    def clear(self) -> "ChainingHashTable[K, V]":
        self._capacity = 4
        self._hash_table = self._init_new_list(self._capacity)

        return self

    def to_array(self) -> list[ChainingHashTableListValue[K, V]]:
        result_arr = []

        for list_item in self._hash_table:
            for item in list_item:
                result_arr.append((item.value.key, item.value.value))

        return result_arr

    def __len__(self):
        return self._size

    def __iter__(self):
        self._iteration_hash_pointer = 0
        self._iteration_node_pointer = None
        self._array_representation = self.to_array()

    def __next__(self) -> ChainingHashTableListValue[K, V]:
        if self._iteration_hash_pointer > self._size:
            raise StopIteration

        item = self._array_representation[self._iteration_hash_pointer]
        self._iteration_hash_pointer += 1

        return item

    def __repr__(self) -> str:
        return str(self._hash_table)
