import pytest
import numpy as np

from type_presentation import AdjacencyMatrix, IncidenceMatrix, AdjacencyList, EdgeList


def _test_all_methods(obj):
    try:
        res = len(obj.nodes())
        assert res != 0
    except Exception as e:
        pytest.fail(f"При возврате узлов графа произошла ошибка")
    try:
        # случайная генерация с малой долей вертяности может вернуть строчку с 0 
        # поэтому не проверяем результат
        res = len(obj.connections(0)) 
    except Exception as e:
        pytest.fail(f"При возврате соединений произошла ошибка")
    try:
        res = obj.weight(0, 0)
    except Exception as e:
        pytest.fail(f"При возврате весов графа произошла ошибка")
    try:
        res = obj.shape()
    except Exception as e:
        pytest.fail(f"При возврате размера графа произошла ошибка")

params = [(i, i) for i in range(2, 20)]
@pytest.mark.parametrize("rows, cols", params)
def test_adjacency_matrix(rows, cols):
    obj = AdjacencyMatrix(
        array = np.random.randint(0, 6, size=(rows, cols))
    )
    _test_all_methods(obj)


params = [i for i in range(2, 20)]
@pytest.mark.parametrize("rows", params)
def test_incidence_matrix(rows):
    obj = IncidenceMatrix(
        array = np.random.randint(-1, 6, 
                                  size=(rows,
                                        rows + np.random.randint(0, rows)))
    )
    _test_all_methods(obj)

params = [i for i in range(2, 20)]
@pytest.mark.parametrize("nodes", params)
def test_adjacency_list(nodes):
    adjacency_list = []
    for _ in range(nodes):
        num_neighbors = np.random.randint(1, nodes - 1)  # Случайное количество соседей
        neighbors = [(np.random.randint(0, nodes - 1),
            np.random.randint(1, 5)) for _ in range(num_neighbors)]
        adjacency_list.append(neighbors)
    
    obj = AdjacencyList(
        adjacency_list
    )
    _test_all_methods(obj)

# params = [i for i in range(2, 20)]

# @pytest.mark.parametrize("nodes", params)
# def test_edge_list(nodes):
#     edges = []
#     for _ in range(np.random.randint(1, nodes)):  # Случайное количество рёбер
#         node1 = np.random.randint(0, nodes)  # Первая вершина
#         node2 = np.random.randint(0, nodes)  # Вторая вершина (может быть другой или той же)
#         while node1 == node2:  # Чтобы избежать петель (если не нужны)
#             node2 = np.random.randint(0, nodes)
        
#         weight = np.random.randint(1, 6)  # Вес ребра
#         edges.append([node1, node2, weight])

#     edges = np.array(edges)  # Преобразуем в массив NumPy для удобства

#     # Здесь можно создать объект AdjacencyList или работать с Edge List напрямую
#     obj = EdgeList(edges)
#     _test_all_methods(obj)

