from typing import TypeVar, Generic, Union, cast, Callable
from ..linked_list import DoublyLinkedList, Node
from collections import deque
from graphviz import Graph

K = TypeVar("K", int, str)
V = TypeVar("V", int, str)


class GraphEdge(Generic[K]):
    def __init__(self, target_vertex_key: K, other_side_edge: Union[Node["GraphEdge[K]"], None] = None) -> None:
        self._target_vertex_key = target_vertex_key
        self._other_side_edge = other_side_edge

    @property
    def target_vertex_key(self) -> K:
        return self._target_vertex_key

    @property
    def other_side_edge(self) -> Union[Node["GraphEdge[K]"], None]:
        return self._other_side_edge

    @other_side_edge.setter
    def other_side_edge(self, node: Union[Node["GraphEdge[K]"], None]) -> Union[Node["GraphEdge[K]"], None]:
        self._other_side_edge = node

        return self._other_side_edge


class GraphVertex(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self._key = key
        self._value = value
        self._adjacency_list = DoublyLinkedList[GraphEdge[K]]()

    @property
    def key(self) -> K:
        return self._key

    @property
    def value(self) -> V:
        return self._value

    @value.setter
    def value(self, new_value: V) -> V:
        self._value = new_value

        return self._value

    @property
    def adjacency_list(self) -> DoublyLinkedList[GraphEdge[K]]:
        return self._adjacency_list


class AdjacencyListGraph(Generic[K, V]):
    def __init__(self, directed: bool = False) -> None:
        self._vertices: dict[K, GraphVertex[K, V]] = dict()
        self._directed = directed

    def add_vertex(self, key: K, value: V) -> "AdjacencyListGraph[K, V]":
        if self._vertices.get(key):
            return self

        self._vertices[key] = GraphVertex(key=key, value=value)

        return self

    def delete_vertex(self, key: K) -> "AdjacencyListGraph[K, V]":
        if not self._vertices.get(key):
            return self

        for adjacent in self._vertices[key].adjacency_list:
            if adjacent.value.other_side_edge:
                self._vertices[adjacent.value.target_vertex_key].adjacency_list.remove_node(
                    node=adjacent.value.other_side_edge
                )

        del self._vertices[key]

        return self

    def add_edge(self, vertex_a_key: K, vertex_b_key: K) -> "AdjacencyListGraph[K, V]":
        if not (self._vertices.get(vertex_a_key) and self._vertices.get(vertex_b_key)):
            return self

        edge_a_to_b = GraphEdge(target_vertex_key=vertex_b_key)
        edge_b_to_a = GraphEdge(target_vertex_key=vertex_a_key)

        # Set other_side_edge for Undirected graphs
        if not self._directed:
            edge_a_to_b.other_side_edge = Node(value=edge_b_to_a)
            edge_b_to_a.other_side_edge = Node(value=edge_a_to_b)

        self._vertices[vertex_a_key].adjacency_list.append(value=edge_a_to_b)
        self._vertices[vertex_b_key].adjacency_list.append(value=edge_b_to_a)

        return self

    def _get_edge_search_function(self, target_vertex_key: K):
        return lambda graphEdge: cast(GraphEdge[K], graphEdge).target_vertex_key == target_vertex_key

    def delete_edge(self, vertex_a_key: K, vertex_b_key: K) -> "AdjacencyListGraph":
        if not (self._vertices.get(vertex_a_key) and self._vertices.get(vertex_b_key)):
            return self

        target_edge = self._vertices[vertex_a_key].adjacency_list.search_node(
            search_func=self._get_edge_search_function(target_vertex_key=vertex_b_key)
        )

        if target_edge is None:
            return self

        self._vertices[vertex_a_key].adjacency_list.remove_node(target_edge)

        if target_edge.value.other_side_edge:
            self._vertices[vertex_b_key].adjacency_list.remove_node(target_edge.value.other_side_edge)

        return self

    def bfs(
        self,
        start_from_vertex_key: K,
        process_vertex_early: Union[Callable[[GraphVertex[K, V]], None], None] = None,
        process_edge: Union[Callable[[GraphVertex[K, V], GraphEdge[K]], None], None] = None,
        process_vertex_late: Union[Callable[[GraphVertex[K, V]], None], None] = None,
        discovered: dict[K, bool] = dict(),
        processed: dict[K, bool] = dict(),
        parent: dict[K, K] = dict(),
    ):
        queue = deque([start_from_vertex_key])

        discovered[start_from_vertex_key] = True

        while len(queue) != 0:
            vertex_key = queue.popleft()

            target_vertex = self._vertices.get(vertex_key)

            if not target_vertex:
                raise ValueError(f"Trying to access the vertex that doesn't exists; vertex_key = {vertex_key}")

            if process_vertex_early:
                process_vertex_early(target_vertex)

            processed[vertex_key] = True

            edge_to_process = target_vertex.adjacency_list.head_node

            while edge_to_process is not None:
                edge = edge_to_process.value

                if (not processed.get(edge.target_vertex_key) or self._directed) and process_edge:
                    process_edge(target_vertex, edge)

                if not discovered.get(edge.target_vertex_key):
                    discovered[edge.target_vertex_key] = True
                    parent[edge.target_vertex_key] = vertex_key
                    queue.append(edge.target_vertex_key)

                edge_to_process = edge_to_process.next

            if process_vertex_late:
                process_vertex_late(target_vertex)

    def export_to_image(self, filename: Union[str, None] = None):
        discovered: dict[K, bool] = dict()
        graph = Graph(graph_attr=[("nodesep", "0.4"), ("ranksep", "0.5")])

        def process_vertex_early(vertex: GraphVertex):
            graph.node(name=str(vertex.key), label=f"value={vertex.value}")

        def process_edge(vertex: GraphVertex, edge: GraphEdge):
            graph.edge(tail_name=str(vertex.key), head_name=str(edge.target_vertex_key))

        # Running cycle to cover case where graph has multiple components
        for vertex in self._vertices:
            if discovered.get(vertex):
                continue

            self.bfs(
                start_from_vertex_key=vertex,
                process_vertex_early=process_vertex_early,
                process_edge=process_edge,
                discovered=discovered,
            )

        graph.render(
            filename=filename, format="png", directory="__generated__", view=True, overwrite_source=True, cleanup=True
        )

    def __len__(self):
        return len(self._vertices)
