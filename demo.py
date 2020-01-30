from tkinter import TclError
from queue import PriorityQueue
from graph import Graph
import matplotlib.pyplot as plt


class MinimalSpanningTreeDemo(Graph):
    def __init__(self, graph: Graph):
        super().__init__()
        self.__pq: PriorityQueue = PriorityQueue()
        self.__graph = graph

    def _init_demo(self, start_v_id: int):
        self.vertices = dict()
        self.__pq = PriorityQueue()
        start_v = self.__graph.vertices[start_v_id]
        self.create_vertex(start_v_id)
        for e in start_v.edges:
            self.__pq.put((e.weight, e))

    def _continue_demo(self):
        weight, edge = self.__pq.get()
        if edge.target.id not in self.vertices:
            self.create_vertex(edge.target.id)
            self.create_edge(edge.start.id, edge.target.id, weight)
            for e in edge.target.edges:
                self.__pq.put((e.weight, e))

    def run(self, start_v_id: int):
        self._init_demo(start_v_id)
        self.draw_state_and_wait_for_button_press()
        while not len(self) == len(self.__graph):
            self._continue_demo()
            self.draw_state_and_wait_for_button_press()
        plt.pause(5)
        plt.waitforbuttonpress()

    def draw_state_and_wait_for_button_press(self):
        plt.clf()
        plt.axis('off')
        plt.subplot(121)
        txt = '[' + ', '.join(
            [f'({e.start.id}, {e.target.id}, W{e.weight})' for w, e in
             self.__pq.queue]) + ']'
        if len(self) == len(self.__graph):
            txt += '\nKONIEC'
        self.__graph.draw()
        plt.text(0, .95, txt, ha='center',
                 va='center')
        plt.subplot(122)
        self.draw(pos=self.__graph.pos)
        plt.waitforbuttonpress()


def get_example_graph():
    g = Graph()
    for i in range(1, 7):
        g.create_vertex(i)
    g.create_edge(1, 2, 4)
    g.create_edge(2, 3, 2)
    g.create_edge(3, 4, 8)
    g.create_edge(4, 5, 3)
    g.create_edge(4, 6, 6)
    g.create_edge(5, 6, 7)
    g.create_edge(6, 1, 2)
    g.create_edge(1, 5, 1)
    g.create_edge(2, 5, 2)
    return g


if __name__ == '__main__':
    try:
        demo = MinimalSpanningTreeDemo(get_example_graph())
        demo.run(1)
    except TclError:
        pass
