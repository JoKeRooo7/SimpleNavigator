import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from type_presentation import AdjacencyMatrix, IncidenceMatrix, AdjacencyList, EdgeList


class NetworxGraphVisualizer():
    def __init__(
            self, 
            data, 
            node_shape='o', 
            node_color='white', 
            edge_color='black', 
            arrow_color='red',
            text_nodes_color="black",
            text_edge_color="black",
            plot_sleep=1):
        self.data = data
        self.graph = nx.DiGraph()
        self.node_shape = node_shape
        self.node_color = node_color
        self.edge_color = edge_color
        self.arrow_color = arrow_color 
        self.text_nodes_color = text_nodes_color
        self.text_edge_color = text_edge_color
        self.plot_sleep = plot_sleep
        self.pos = None  # Позиции узлов, задаваемые layout
        self._build_graph()
        self.layout = 'spring'

    def _build_graph(self):
        """Построение графа на основе матрицы смежности."""

        for i in self.data.nodes():
            if not self.graph.has_node(i):
                self.graph.add_node(i)

        for i in self.data.nodes():   
            for j in self.data.connections(index=i):
                self.graph.add_edge(i, j, weight=self.data.weight(i, j))
        # print(self.graph.nodes())
        # print(self.graph.edges(data=True)) 

    def draw_graph(self, layout=None, node_size=500, font_size=12, node_color=None, edge_color=None):
        """Визуализация графа с выбранным layout и параметрами."""
        plt.clf()  # Очистка текущего графика
        plt.figure(figsize=(8, 8))

        # Если layout не задан, используем сохранённый
        if layout is not None:
            self.layout = layout

        # Выбор раскладки для узлов
        if self.layout == 'spring':
            self.pos = nx.spring_layout(self.graph)  # Spring layout
        elif self.layout == 'circular':
            self.pos = nx.circular_layout(self.graph)  # Circular layout
        elif self.layout == 'random':
            self.pos = nx.random_layout(self.graph)  # Random layout
        elif self.layout == 'shell':
            self.pos = nx.shell_layout(self.graph)  # Shell layout
        elif self.layout == 'spectral':
            self.pos = nx.spectral_layout(self.graph)  # Spectral layout

        # Если цвета узлов или рёбер не заданы, используем стандартные
        if node_color is None:
            node_color = self.node_color
        if edge_color is None:
            edge_color = self.edge_color

        # Отрисовка узлов
        if self.node_shape == 'o':  # Круги
            self.node_collection = nx.draw_networkx_nodes(
                self.graph, 
                self.pos, 
                node_size=node_size, 
                node_color=node_color,  # Используем переданный цвет
                edgecolors=self.edge_color,  
                linewidths=1
            )
        elif self.node_shape == 's':  # Квадраты
            self.node_collection = nx.draw_networkx_nodes(
                self.graph, 
                self.pos, 
                node_size=node_size, 
                node_color=node_color,  
                edgecolors=self.edge_color,  
                linewidths=1, 
                marker='s'
            )

        # Отрисовка рёбер
        nx.draw_networkx_edges(self.graph, self.pos, edge_color=edge_color, arrows=True, arrowstyle='-|>', arrowsize=20)

        # Отрисовка меток узлов (индексы узлов)
        nx.draw_networkx_labels(self.graph, self.pos, font_size=font_size, font_color=self.text_nodes_color)

        # Отрисовка весов рёбер
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, font_color=self.text_edge_color)

        plt.title(f'Graph Visualization using {self.layout} layout')
        plt.axis('off')  # Отключаем оси
        plt.show(block=False)
        plt.pause(self.plot_sleep)
   
    def update_graph(self, path, current_index, path_color="red", index_color="green"):
        """Обновляет визуализацию графа, выделяя текущую вершину и путь."""
        
        # Задаём цвета узлов для пути и текущего индекса
        node_colors = {node: path_color for node in path}
        node_colors[current_index] = index_color

        # Присваиваем цвета для каждого узла
        colors = [node_colors.get(node, self.node_color) for node in self.graph.nodes()]

        # Заново рисуем узлы с обновлёнными цветами
        plt.clf()  # Очищаем текущее изображение
        self.node_collection = nx.draw_networkx_nodes(
            self.graph, 
            self.pos, 
            node_color=colors,  # Применяем новые цвета
            node_size=500, 
            edgecolors=self.edge_color,  
            linewidths=1
        )
        
        # Заново рисуем рёбра и метки
        nx.draw_networkx_edges(self.graph, self.pos, edge_color=self.edge_color, arrows=True, arrowstyle='-|>', arrowsize=20)
        nx.draw_networkx_labels(self.graph, self.pos, font_size=12, font_color=self.text_nodes_color)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, font_color=self.text_edge_color)
        # Отображаем изменения
        plt.title(f'Graph Visualization using {self.layout} layout')
        plt.axis('off')  # Отключаем оси
        plt.show(block=False)

        plt.pause(self.plot_sleep)

   


class GraphVisualizer():
    def __init__(self, data, radius=0.3):
        self.data = data
        self.radius = radius
        self.radius_shift = radius * 2 + 1
        self.coordinates = None

    def _calculate_x(self, x, idxnumber, size_indexes, horizontal_shift=0):
        if size_indexes % 2 == 0:
            additional_shift = 0.5
            is_more_median = (idxnumber >= size_indexes // 2)
            additional_shift = additional_shift if is_more_median else -additional_shift
            need_shift = (size_indexes // 2 - idxnumber + additional_shift) * self.radius_shift + horizontal_shift
            if x > 0:
                x += need_shift if is_more_median else -need_shift
            else:
                x -= need_shift if is_more_median else -need_shift
        elif idxnumber == size_indexes // 2:
            pass
        else:
            need_shift = (size_indexes // 2 - idxnumber) * self.radius_shift + horizontal_shift
            is_more_median = (idxnumber >= size_indexes // 2)
            if x > 0:
                x += need_shift if is_more_median else -need_shift
            else:
                x -= need_shift if is_more_median else -need_shift
            x += need_shift if x > 0 else -need_shift
        return x

    def generate_coordinates(self, data=None, horizontal_shift=2, ):
        if data is not None:
            self.data = data
    
        coordinates = {}
        for i in range(len(self.data)):
            if i in coordinates:
                continue
            elif not coordinates:
                coordinates[i] = (0, 0)
            else:
                x, y = coordinates[list(coordinates.keys())[-1]]
                coordinates[i] = (x, y - 1 - self.radius_shift)
            indexes = self.data.indexes(i)
            size_indexes = len(indexes)
            print(size_indexes)
            for j, index in enumerate(indexes):
                if index in coordinates:
                    continue
                x, y = coordinates[i]

                new_x = self._calculate_x(x=x, idxnumber=j, size_indexes=size_indexes, horizontal_shift=horizontal_shift)
                y = y - 1 - self.radius_shift
                coordinates[index] = (x, y)
        self.coordinates = coordinates
        return self.coordinates
    
    def draw_nodes(self):
        """Рисует узлы графа (кружки) с их номерами на координатах."""
        for node, (x, y) in self.coordinates.items():
            # Рисуем кружок
            circle = plt.Circle((x, y), self.radius, edgecolor='black', fill=False)
            self.ax.add_artist(circle)
            
            # Добавляем номер узла в центр кружка
            self.ax.text(x, y, str(node), fontsize=12, ha='center', va='center', color='black')  
    
    def draw_graph(self, data=None):
        if data is not None:
            self.data = data
        self.ig, self.ax = plt.subplots()

        coordinates = self.generate_coordinates()
        self.draw_nodes()
        self.draw_edges()

        # Настройки графика
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-5, 5)  # Задайте пределы графика
        self.ax.set_ylim(-5, 5)
        self.ax.axis('off')  # Скрыть оси
            # Показываем график
        plt.show()

    # def draw_edges(self):
    #     """Рисует рёбра графа в виде стрелок, оканчивающихся на границе круга."""
    #     for i in range(len(self.data)):
    #         indexes = self.data.indexes(i)
    #         x_start, y_start = self.coordinates[i]
            
    #         for index in indexes:
    #             x_end, y_end = self.coordinates[index]

    #             # Вычисляем направление стрелки
    #             dx = x_end - x_start
    #             dy = y_end - y_start
    #             distance = np.hypot(dx, dy)  # Расстояние между узлами

    #             # Смещаем конечную точку стрелки до границы окружности
    #             x_end_shifted = x_end - (self.radius / distance) * dx
    #             y_end_shifted = y_end - (self.radius / distance) * dy

    #             # Смещаем начальную точку стрелки до границы окружности
    #             x_start_shifted = x_start + (self.radius / distance) * dx
    #             y_start_shifted = y_start + (self.radius / distance) * dy

    #             # Рисуем стрелку
    #             self.ax.annotate("",
    #                              xy=(x_end_shifted, y_end_shifted),  # Конечная точка
    #                              xytext=(x_start_shifted, y_start_shifted),  # Начальная точка
    #                              arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))
    def draw_edges(self):
            """Рисует изогнутые рёбра графа с помощью дуг."""
            for i in range(len(self.data)):
                indexes = self.data.indexes(i)
                x_start, y_start = self.coordinates[i]
                
                for index in indexes:
                    x_end, y_end = self.coordinates[index]

                    # Вычисляем направление стрелки
                    dx = x_end - x_start
                    dy = y_end - y_start
                    distance = np.hypot(dx, dy)  # Расстояние между узлами

                    # Смещаем конечную точку стрелки до границы окружности
                    x_end_shifted = x_end - (self.radius / distance) * dx
                    y_end_shifted = y_end - (self.radius / distance) * dy

                    # Смещаем начальную точку стрелки до границы окружности
                    x_start_shifted = x_start + (self.radius / distance) * dx
                    y_start_shifted = y_start + (self.radius / distance) * dy

                    # Рисуем изогнутую стрелку с помощью дуги
                    self.ax.annotate("",
                                    xy=(x_end_shifted, y_end_shifted),  # Конечная точка
                                    xytext=(x_start_shifted, y_start_shifted),  # Начальная точка
                                    arrowprops=dict(arrowstyle="->", lw=1.5, color="black",
                                                    connectionstyle="arc3,rad=0.2"))  # Изгиб дуги



# # Вызов функции для рисования графа