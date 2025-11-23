from queue import PriorityQueue
from collections import defaultdict

class Agente:  
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal   
        
        self.PATH = 0
        self.WALL = 1
        
        # armazena explorados
        self.path = []
        self.explored_nodes = set()
        
        # Estruturas de dados do A*
        self.open_set = PriorityQueue()
        self.came_from = {}
        
        self.g_score = defaultdict(lambda: float('inf'))
        self.g_score[self.start] = 0
        
        self.f_score = defaultdict(lambda: float('inf'))
        self.f_score[self.start] = self._calculate_heuristic(self.start)

        # add no inicial
        self.open_set.put((self.f_score[self.start], self.start))

        self.status = "searching" 

    def _calculate_heuristic(self, node):
        (y1, x1) = node
        (y2, x2) = self.goal
        return abs(y1 - y2) + abs(x1 - x2)

    def _get_neighbors(self, node):
        (y, x) = node
        neighbors = []
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx

            # verifica se vizinho dentro limites labirinto
            if 0 <= ny < self.maze.shape[0] and 0 <= nx < self.maze.shape[1]:

                # verifica se vizinho = caminho ou parede
                if self.maze[ny, nx] == self.PATH:
                    neighbors.append((ny, nx))
        return neighbors

    def _reconstruct_path(self):
        current = self.goal
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)

        # inverte lista p/ (ini -> obj)
        self.path = path[::-1]

    def solve_step(self):
        # checa status
        if self.status != "searching":
            return self.status

        # se fila vazia finaliza
        if self.open_set.empty():
            self.status = "no_path"
            return self.status

        # pega menor no
        current_f, current = self.open_set.get()

        # add no atual explorados
        self.explored_nodes.add(current)

        # testa se objetivo    
        if current == self.goal:
            self._reconstruct_path()
            self.status = "goal_found"
            return self.status

        # se != objetivo verifica vizinhos    
        for neighbor in self._get_neighbors(current):
            tentative_g_score = self.g_score[current] + 1
            
            if tentative_g_score < self.g_score[neighbor]:
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g_score
                self.f_score[neighbor] = tentative_g_score + self._calculate_heuristic(neighbor)
                
                # add vizinho a fila para explorar
                self.open_set.put((self.f_score[neighbor], neighbor))
        
        return self.status