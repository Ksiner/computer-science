from unittest import TestCase as UnitTestCase
from .adjacency_list_graph import AdjacencyListGraph
from .adjacency_matrix_graph import AdjacencyMatrixGraph


class AdjacencyMatrixGraphTests(UnitTestCase):
    def test_graph(self):
        matrix_graph = AdjacencyMatrixGraph(10)

        self.assertEqual(len(matrix_graph), 10)
        self.assertEqual(len(matrix_graph._adjacent_matrix[0]), 10)
        self.assertEqual(len(matrix_graph._adjacent_matrix[9]), 10)

        matrix_graph.add_vertex()

        self.assertEqual(len(matrix_graph), 11)
        self.assertEqual(len(matrix_graph._adjacent_matrix[10]), 11)

        matrix_graph.delete_vertex(10)

        self.assertEqual(len(matrix_graph), 10)

        matrix_graph.add_edge(0, 1)
        self.assertEqual(matrix_graph._adjacent_matrix[0][1], 1)
        self.assertEqual(matrix_graph._adjacent_matrix[1][0], 1)
        self.assertEqual(matrix_graph._adjacent_matrix[1][1], 0)
        self.assertEqual(matrix_graph._adjacent_matrix[2][1], 0)
        self.assertEqual(matrix_graph._adjacent_matrix[3][0], 0)

        matrix_graph.delete_edge(0, 1)
        self.assertEqual(matrix_graph._adjacent_matrix[0][1], 0)
        self.assertEqual(matrix_graph._adjacent_matrix[1][0], 0)


class AdjacencyListGraphTests(UnitTestCase):
    def test_undirected_graph(self):
        # Graph Init
        list_graph = AdjacencyListGraph[int, str]()
        list_graph.add_vertex(1, "first")
        list_graph.add_vertex(2, "second")

        self.assertEqual(len(list_graph), 2)

        # Add edge
        list_graph.add_edge(1, 2)

        self.assertEqual(len(list_graph._vertices[1].adjacency_list), 1)

        if not list_graph._vertices[1].adjacency_list.head:
            raise self.failureException('Missing head on adjacency list of the "first" vertex')

        self.assertEquals(list_graph._vertices[1].adjacency_list.head.target_vertex_key, 2)
        self.assertIsNotNone(list_graph._vertices[1].adjacency_list.head.other_side_edge)

        self.assertEqual(len(list_graph._vertices[2].adjacency_list), 1)

        if not list_graph._vertices[2].adjacency_list.head:
            raise self.failureException('Missing head on adjacency list of the "second" vertex')

        self.assertEquals(list_graph._vertices[2].adjacency_list.head.target_vertex_key, 1)
        self.assertIsNotNone(list_graph._vertices[2].adjacency_list.head.other_side_edge)

        # Removing edge
        list_graph.delete_edge(1, 2)

        self.assertEqual(len(list_graph._vertices[1].adjacency_list), 0)
        self.assertEqual(len(list_graph._vertices[2].adjacency_list), 0)
        self.assertIsNone(list_graph._vertices[1].adjacency_list.head)
        self.assertIsNone(list_graph._vertices[2].adjacency_list.head)

        # Removing vertex
        list_graph.delete_vertex(1)

        self.assertEqual(len(list_graph), 1)
        self.assertIsNone(list_graph._vertices.get(1))
        self.assertIsNotNone(list_graph._vertices[2])

        # Removing vertex with edges

        list_graph.add_vertex(1, "first")
        list_graph.add_edge(1, 2)
        list_graph.delete_vertex(1)

        self.assertIsNone(list_graph._vertices.get(1))
        self.assertIsNotNone(list_graph._vertices[2])
        self.assertEqual(len(list_graph._vertices[2].adjacency_list), 0)
        self.assertIsNone(list_graph._vertices[2].adjacency_list.head)

    def test_bfs(self):
        list_graph = AdjacencyListGraph[int, str]()
        # Adding vertices
        list_graph.add_vertex(1, "first").add_vertex(2, "second").add_vertex(3, "third").add_vertex(
            4, "fourth"
        ).add_vertex(5, "fifth").add_vertex(6, "sixth").add_vertex(7, "seventh").add_vertex(8, "eight")

        # Adding edges
        list_graph.add_edge(1, 8).add_edge(1, 7).add_edge(1, 2).add_edge(2, 7).add_edge(2, 3).add_edge(2, 5).add_edge(
            5, 3
        ).add_edge(3, 4).add_edge(5, 4).add_edge(5, 6)

        discovered: dict[int, bool] = dict()
        processed: dict[int, bool] = dict()
        parent: dict[int, int] = dict()

        list_graph.bfs(1, discovered=discovered, processed=processed, parent=parent)

        self.assertDictEqual(discovered, {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True})
        self.assertDictEqual(processed, {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True})
        self.assertDictEqual(parent, {2: 1, 3: 2, 4: 3, 5: 2, 6: 5, 7: 1, 8: 1})
