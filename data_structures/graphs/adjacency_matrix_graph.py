class AdjacencyMatrixGraph:
    def __init__(self, vertices_count: int) -> None:
        self._vertices_count = vertices_count
        self._edges_count: int = 0
        self._adjacent_matrix: list[list[int]] = [
            [0 for i in range(0, vertices_count)] for i in range(0, vertices_count)
        ]

    def _vertex_key_is_in_bound(self, vertex_key: int) -> bool:
        return vertex_key >= 0 or vertex_key < len(self._adjacent_matrix)

    def add_vertex(self) -> "AdjacencyMatrixGraph":
        self._vertices_count += 1

        for adjacent in self._adjacent_matrix:
            adjacent.append(0)

        self._adjacent_matrix.append([0] * self._vertices_count)

        return self

    def delete_vertex(self, vertex_key: int) -> "AdjacencyMatrixGraph":
        if not self._vertex_key_is_in_bound(vertex_key=vertex_key):
            return self

        for adjacent in self._adjacent_matrix:
            adjacent.pop(vertex_key)

        self._adjacent_matrix.pop(vertex_key)

        self._vertices_count -= 1

        return self

    def add_edge(self, vertex_a_key: int, vertex_b_key: int) -> "AdjacencyMatrixGraph":
        if not (
            self._vertex_key_is_in_bound(vertex_key=vertex_a_key)
            and self._vertex_key_is_in_bound(vertex_key=vertex_b_key)
        ):
            return self

        if (
            self._adjacent_matrix[vertex_a_key][vertex_b_key] != 1
            and self._adjacent_matrix[vertex_b_key][vertex_a_key] != 1
        ):
            self._adjacent_matrix[vertex_a_key][vertex_b_key] = 1
            self._adjacent_matrix[vertex_b_key][vertex_a_key] = 1

            self._edges_count += 1

        return self

    def delete_edge(self, vertex_a_key: int, vertex_b_key: int) -> "AdjacencyMatrixGraph":
        if not (
            self._vertex_key_is_in_bound(vertex_key=vertex_a_key)
            and self._vertex_key_is_in_bound(vertex_key=vertex_b_key)
        ):
            return self

        if (
            self._adjacent_matrix[vertex_a_key][vertex_b_key] != 0
            or self._adjacent_matrix[vertex_b_key][vertex_a_key] != 0
        ):
            self._adjacent_matrix[vertex_a_key][vertex_b_key] = 0
            self._adjacent_matrix[vertex_b_key][vertex_a_key] = 0

            self._vertices_count -= 1

        return self

    def __len__(self):
        return self._vertices_count
