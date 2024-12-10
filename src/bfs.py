import numpy as np
from queue import Queue
from type_presentation import AdjacencyMatrix, IncidenceMatrix, AdjacencyList, EdgeList


class BFS():
    def __init__(self, data):
        self.data = data

    @property
    def data(self) -> AdjacencyMatrix:
        return self.__data

    def data(self, data) -> None:
        if data is not None:
            self.__data = data
    
    def _check_type(self, data):
        if not isinstance(data, (AdjacencyMatrix, IncidenceMatrix, AdjacencyList, EdgeList)):
            raise TypeError(f"Type {data}: not correct")

    def _need_elements(self, index):
        # Возращаем элементы по данному индексу
        if isinstance(self.data, AdjacencyMatrix):
            # в матрице смежности у текущего узла возращаем все соединенные графы
            return np.nonzero(self.data[index])[0]
        elif isinstance(self.data, IncidenceMatrix):
            # в матрица инцидентности сначала находим все исходящие ребра, потом находим все индексы куда входят эти ребра
            filtered_indices = np.where((self.data[index] != 0) & (self.data[index] != -1))[0]
            rows_with_non_zero = np.where((self.data[:, filtered_indices] != 0))[0]
            return rows_with_non_zero
        elif isinstance(self.data, AdjacencyList):
            # в списке смежности уже и так даны соседи, просто возращаем их 
            return self.data[index]
        elif isinstance(self.data, EdgeList):
            # в списке ребер возрашаем все строки с текущим индексом потом возрашаем все соендинные вершины
            indexes = np.where(self.data[:, 0] == index)[0]
            return self.data[indexes, 1]
        else:
            raise TypeError(f"invalid data type ({type(self.data)})")

    def finding_way(self, vertices:tuple, data=None) -> list:
        if data is not None:
            self.data = data
        start, end = vertices
        ways = Queue()
        ways.put((start, [start]))
        while not ways.empty():
            index, way = ways.get()
            if index == end:
                return way

            need_indexes = self._need_elements(index)
            for new_index in need_indexes:
                # костыль для AdjacencyList
                if isinstance(new_index, tuple):
                    new_index, _ = new_index
                if new_index not in way:
                    ways.put((new_index, way + [new_index]))
        return None


if __name__ == "__main__":
    matrix = np.array([[0, 1, 2, 0],
                      [0, 4, 5, 0],
                      [6, 0, 0, 8]])
    matrix = AdjacencyMatrix(matrix)
    my_class = BFS(matrix)
    
    print(my_class.finding_way((0, 3)))

    incidence_matrix = np.array([

        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Вершина 0
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # Вершина 1
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],  # Вершина 2
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],  # Вершина 3
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],  # Вершина 4
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]   # Вершина 5
    ])

    incidence_matrix = IncidenceMatrix(incidence_matrix)
    my_class = BFS(incidence_matrix)
    print(my_class.finding_way((0, 4)))


    adjacency_list_with_weights = [
        [(1, 4), (2, 1), (3, 3)],   # Вершина 0 соединена с 1 (вес 4), 2 (вес 1), 3 (вес 3)
        [(0, 4), (3, 2)],           # Вершина 1 соединена с 0 (вес 4), 3 (вес 2)
        [(0, 1), (3, 5)],           # Вершина 2 соединена с 0 (вес 1), 3 (вес 5)
        [(0, 3), (1, 2), (5, 6)],   # Вершина 3 соединена с 0 (вес 3), 1 (вес 2), 5 (вес 6)
        [(2, 4), (5, 2)],           # Вершина 4 соединена с 2 (вес 4), 5 (вес 2)
        [(3, 6), (4, 2)]            # Вершина 5 соединена с 3 (вес 6), 4 (вес 2)
    ]
    adjacency_list_with_weights = AdjacencyList(adjacency_list_with_weights)
    my_class = BFS(adjacency_list_with_weights)

    print(my_class.finding_way((0, 5)))

    edges = np.array([
        [0, 1, 5],  # Ребро между вершинами 0 и 1 с весом 5
        [0, 2, 10], # Ребро между вершинами 0 и 2 с весом 10
        [1, 3, 7],  # Ребро между вершинами 1 и 3 с весом 7
        [2, 3, 3],  # Ребро между вершинами 2 и 3 с весом 3
        [3, 4, 2]   # Ребро между вершинами 3 и 4 с весом 2
    ])

    edges = EdgeList(edges)

    my_class = BFS(edges)

    print(my_class.finding_way((0, 4)))


