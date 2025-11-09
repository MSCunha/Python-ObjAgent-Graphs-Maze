import random
import numpy as np
from mazeGen import MazeGenerator
from grafos import MazeToGraph
from pathFinder import PathFinder

class MazeSolverAgent:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed

        self.maze = None
        self.graph = None
        self.start_pos = None
        self.goal_pos = None
        self.pathfinder = None
        

        self.results = {
            'algorithms': {}
        }

    def initialize_environment(self):
        print(f"\n→ [Agente] Gerando labirinto {self.width}x{self.height}...")
        gen = MazeGenerator(width=self.width, height=self.height, seed=self.seed)
        self.maze = gen.generate()
        
        possible_start = (1, 1)
        y_indices, x_indices = np.where(self.maze == gen.PATH)
        valid_coords = list(zip(y_indices, x_indices))
        
        if possible_start in valid_coords:
            self.start_pos = possible_start
            valid_coords.remove(self.start_pos)
        else:
            self.start_pos = valid_coords.pop(0)
            
        rng = random.Random(self.seed)
        self.goal_pos = rng.choice(valid_coords)
        
        print(f"→ [Agente] Posição inicial definida: {self.start_pos}")
        print(f"→ [Agente] Posição objetivo definida: {self.goal_pos}")
        
        self.results['start'] = self.start_pos
        self.results['goal'] = self.goal_pos

        self._validate_environment()

        print(f"\n→ [Agente] Convertendo labirinto para grafo NetworkX...")
        graph_builder = MazeToGraph(self.maze)
        self.graph = graph_builder.build_graph()
        print(f"✓ [Agente] Grafo criado: {self.graph.number_of_nodes()} nós, {self.graph.number_of_edges()} arestas")

        self.pathfinder = PathFinder(self.graph, self.start_pos, self.goal_pos)

    def _validate_environment(self):
        PATH = 0
        if self.maze[self.start_pos[0], self.start_pos[1]] != PATH:
            raise ValueError(f"Posição inicial {self.start_pos} é inválida (parede)")
        if self.maze[self.goal_pos[0], self.goal_pos[1]] != PATH:
            raise ValueError(f"Posição objetivo {self.goal_pos} é inválida (parede)")
        if self.start_pos == self.goal_pos:
            raise ValueError("Início e objetivo não podem ser iguais")

    def solve_astar(self):
        if not self.pathfinder:
            raise RuntimeError("Ambiente não inicializado. Chame initialize_environment() primeiro.")
            
        print(f"\n→ [Agente] Executando A*...")
        astar_result = self.pathfinder.run_astar()
        self.results['algorithms']['A*'] = astar_result
        return astar_result

    def compare_algorithms(self):
        if not self.pathfinder:
            raise RuntimeError("Ambiente não inicializado.")
            
        print(f"\n→ [Agente] Executando comparação de algoritmos...")
        comparison = self.pathfinder.compare_algorithms()
        
        for algo_name, algo_data in comparison.items():
             self.results['algorithms'][algo_name] = algo_data
             
        return comparison

    def print_comparison_table(self, comparison_results):
        if self.pathfinder:
            self.pathfinder.print_comparison_table(comparison_results)