import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Graph:
    def __getitem__(self, index):
        pass
    
    def __len__(self):
        pass
    
    def __iter__(self):
        pass
    
    def nodes(self):
        pass

    def connections(self, index):
        pass
    
    def weight(self, i, j):
        pass

    @property
    def shape(self):
        pass

@dataclass
class AdjacencyMatrix(Graph):
    """
    Матрица смежности

    Матрица смежности — квадратная матрица, размерность которой равна числу вершин в графе, и в которой AijA_{ij}Aij​
    элемент матрицы содержит в себе информацию о ребре из вершины i в вершину j. Возможные значения, которые может принимать AijA_{ij}Aij​:
        для невзвешенного неориентированного графа:
            0 — ребра между вершинами нет
            1 — ребро между вершинами есть
        для взвешенного неориентированного графа:
            0 — ребра между вершинами нет
            N — ребро между вершинами есть, и его вес равен N
        для невзвешенного ориентированного графа:
            0 — дуги между вершинами нет
            1 — есть дуга (ориентированное ребро), которая направлена из вершины i в вершину j
        для взвешенного ориентированного графа:
            0 — дуги между вершинами нет
            N — есть дуга (ориентированное ребро), которая направлена из вершины i в вершину j, и её вес равен N

    Атрибуты:
        matrix (np.ndarray) - матрица смежности
    """
    matrix: np.ndarray

    def __getitem__(self, index):
        return self.matrix[index]
    
    def __len__(self):
        return len(self.matrix)
    
    def __iter__(self):
        return iter(self.matrix)
    
    def nodes(self) -> list:
        return list(range(self.matrix.shape[0])) 

    def connections(self, index):
        return np.nonzero(self.matrix[index])[0]
    
    def weight(self, i, j):
        return self.matrix[i, j]

    @property
    def shape(self):
        """Возвращает размеры матрицы смежности (число вершин, число вершин)"""
        return self.matrix.shape

@dataclass
class IncidenceMatrix(Graph):
    """
    Матрица инцидентности

    Матрица инцидентности — это матрица, количество строк в которой соответствует числу вершин,
    а количество столбцов — числу рёбер.
    В ней указываются связи между инцидентными элементами графа (ребро (дуга) и вершина).
    В неориентированном графе если вершина инцидентна ребру, то соответствующий элемент равен 1, в противном случае элемент равен 0.
    В ориентированном графе если ребро выходит из вершины, то соответствующий элемент равен 1; если ребро входит в вершину,
    то соответствующий элемент равен -1; если ребро отсутствует, то элемент равен 0.

    Атрибуты:
        matrix (np.ndarray) - матрица инцидентности
    """
    matrix: np.ndarray

    def __getitem__(self, index):
        return self.matrix[index]

    def __len__(self):
        return len(self.matrix)  
    
    def nodes(self):
        return list(range(self.matrix.shape[0])) 

    def connections(self, index):
        # надо улучшить, много лишних операций
        outgoing_edges = np.where((self.matrix[index] != 0) & (self.matrix[index] != -1))[0]
        indexes = np.where((self.matrix[:, outgoing_edges] != 0))[0]
        unique_indexes = np.unique(indexes[indexes != index])
        return unique_indexes
    
    def weight(self, i, j):
        outgoing_edges1 = np.where(self.matrix[i] != 0)[0]
        outgoing_edges2 = np.where(self.matrix[j] != 0)[0]
        # фигня костыльная магическая еще и в 1d
        common_edges = np.intersect1d(outgoing_edges1, outgoing_edges2)
        ij_weight = self.matrix[i, common_edges[0]]
        ji_weight = self.matrix[j, common_edges[0]]
        return ij_weight if ij_weight > 0 else ji_weight

    @property
    def shape(self):
        """Возвращает размеры матрицы смежности (число вершин, число вершин)"""
        return self.matrix.shape


@dataclass
class AdjacencyList(Graph):
    """
    Список смежности

    Список смежности — один из способов представления графа в виде коллекции списков вершин.
    Каждой вершине графа соответствует список, состоящий из «соседей» (т. е. из вершин, которые
    непосредственно достижимы напрямую из текущей вершины) этой вершины с указанием весов рёбер.

    Атрибуты:

    """
    _data : List[List[Tuple[int, int]]]
    _data_only_indexes : List[List[int]] = None

    def __post_init__(self):
        self._init_data_only_indexes()

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)  
    
    def nodes(self):
        nodes = set()
        for neighbors in self.data:
            nodes.update(neighbor[0] for neighbor in neighbors)  # Извлекаем первый элемент из каждого кортежа
        return list(nodes) 

    def connections(self, index):
        return self._data_only_indexes[index]
    
    def weight(self, i, j):
        weight_ij = self._find_edge_weight(i, j)
        if weight_ij is not None:
            return weight_ij
        
        weight_ji = self._find_edge_weight(j, i)
        return weight_ji


    @property
    def shape(self):
        """Возвращает размеры матрицы смежности (число вершин, число вершин)"""
        return self.__len__

    @property
    def data(self) -> List[List[Tuple[int, int]]]:
        return self._data

    @data.setter
    def data(self, data: List[List[Tuple[int, int]]]):
        self._data = data
        print(self._data)
        self._init_data_only_indexes()

    def _init_data_only_indexes(self):
        self._data_only_indexes = [[neighbor[0] for neighbor in neighbors] for neighbors in self.data]

    def _find_edge_weight(self, node1: int, node2: int):
        """Найти вес ребра между двумя узлами."""
        for neighbor in self.data[node1]:
            if neighbor[0] == node2:
                return neighbor[1]
        return None


@dataclass
class EdgeList(Graph):
    """
    Список рёбер

    Список рёбер — таблица (матрица размерностью Nx3), в каждой строке которой записаны две смежные
    вершины и вес, соединяющего их ребра.
    """
    matrix: np.ndarray

    def __getitem__(self, index):
        return self.matrix[index]
    
    def __len__(self):
        return len(self.matrix)
    
    def __iter__(self):
        return iter(self.matrix)
    
    def nodes(self) -> list:
        nodes = set()
        for i, j, weight in self.data:
            nodes.update(i)
            nodes.update(j)
        return list(nodes)

    def connections(self, index):
        rows = np.where(self.matrix[:, 0] == index)[0]
        return self.matrix[rows, 1]

    
    def weight(self, i, j):
        сondition = (((self.matrix[:, 0] == i) & (self.matrix[:, 1] == j)) | 
            ((self.matrix[:, 0] == j) & (self.matrix[:, 1] == i)))
        weights = self.matrix[сondition][:, 2]  # Третий столбец (вес)
        return weights

    @property
    def shape(self):
        """Возвращает размеры матрицы смежности (число вершин, число вершин)"""
        return self.matrix.shape
