import networkx as nx
import numpy as np


class MazeToGraph:
    
    PATH = 0
    WALL = 1
    
    def __init__(self, maze):
        self.maze = maze
        self.height, self.width = maze.shape
        self.graph = None
    
    def build_graph(self):

        G = nx.Graph()
        
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y, x] == self.PATH:
                    G.add_node((y, x), pos=(x, y))
        
        for node in G.nodes():
            y, x = node
            
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (y + dy, x + dx)
                
                if neighbor in G.nodes():
                    G.add_edge(node, neighbor, weight=1)
        
        self.graph = G
        return G
    
    def get_node_positions(self):
        if self.graph is None:
            raise ValueError("Grafo ainda não foi construído. Chame build_graph() primeiro.")
        
        return nx.get_node_attributes(self.graph, 'pos')
    
    def get_graph_stats(self):
        if self.graph is None:
            raise ValueError("Grafo ainda não foi construído. Chame build_graph() primeiro.")
        
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'is_connected': nx.is_connected(self.graph),
            'avg_degree': sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
        }
    
    def validate_path_exists(self, start, goal):

        if self.graph is None:
            raise ValueError("Grafo ainda não foi construído. Chame build_graph() primeiro.")
        
        if start not in self.graph.nodes():
            raise ValueError(f"Nó inicial {start} não existe no grafo")
        
        if goal not in self.graph.nodes():
            raise ValueError(f"Nó objetivo {goal} não existe no grafo")
        
        return nx.has_path(self.graph, start, goal)
    