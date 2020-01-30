from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Dict, Set
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'


@dataclass
class Edge:
    start: 'Vertex'
    target: 'Vertex'
    weight: int

    def __lt__(self, other):
        return self.weight < other.weight

    def __hash__(self):
        return self.target.id


@dataclass
class Vertex:
    id: int
    edges: Set['Edge'] = field(default_factory=set)

    def connect(self, v: 'Vertex', weight: int):
        self.edges.add(Edge(self, v, weight))


class Graph:
    def __init__(self):
        self.vertices: Dict[int, 'Vertex'] = dict()
        self.__graph: nx.Graph = nx.Graph()
        self.__pos = nx.spring_layout(self.__graph)

    def create_vertex(self, v_id: int):
        self.vertices[v_id] = Vertex(v_id)

    def create_edge(self, v_id, u_id, weight):
        self.vertices[v_id].connect(self.vertices[u_id], weight)
        self.vertices[u_id].connect(self.vertices[v_id], weight)
        self.__propagate_networkx_graph()

    def __propagate_networkx_graph(self):
        self.__graph = nx.Graph()
        edges = set()
        for v in self.vertices.values():
            for e in v.edges:
                edges.add(tuple(sorted((e.start.id, e.target.id)))
                          + (e.weight,))
        self.__graph.add_weighted_edges_from(edges)
        self.__pos = nx.spring_layout(self.__graph)

    def draw(self, pos=None):
        if not pos:
            pos = self.__pos

        nx.draw(self.__graph, pos, with_labels=True)

        labels = nx.get_edge_attributes(self.__graph, 'weight')
        nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=labels)
        plt.ion()
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()

    @property
    def pos(self):
        return self.__pos

    def __len__(self):
        return len(self.vertices)

    def __contains__(self, index):
        return index in self.vertices


class MinimalSpanningTree(Graph):
    def __init__(self, graph: Graph, start_v_id: int):
        super().__init__()
        pq = PriorityQueue()
        start_v = graph.vertices[start_v_id]
        self.create_vertex(start_v_id)
        for e in start_v.edges:
            pq.put((e.weight, e))
        while not len(self) == len(graph):
            weight, edge = pq.get()
            if edge.target.id not in self.vertices:
                self.create_vertex(edge.target.id)
                self.create_edge(edge.start.id, edge.target.id, weight)
                for e in edge.target.edges:
                    pq.put((e.weight, e))

