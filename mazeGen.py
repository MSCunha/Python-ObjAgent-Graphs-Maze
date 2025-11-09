import random
import numpy as np

class MazeGenerator:
    PATH = 0
    WALL = 1
    
    def __init__(self, width, height, seed=None):
        self.logical_width = width
        self.logical_height = height
        
        self.matrix_width = (width * 2) + 1
        self.matrix_height = (height * 2) + 1
        
        self.seed = seed
        random.seed(self.seed)
        
        self.maze = np.ones((self.matrix_height, self.matrix_width), dtype=np.uint8)
        
        self.visited = np.zeros((self.logical_height, self.logical_width), dtype=bool)
    
    def _is_valid(self, x, y):
        return 0 <= x < self.logical_width and 0 <= y < self.logical_height

    def _carve_passages(self, cx, cy):
        self.visited[cy, cx] = True
        
        mx, my = (cx * 2) + 1, (cy * 2) + 1
        self.maze[my, mx] = self.PATH  
        
        neighbors = [(0, -1), (0, 1), (1, 0), (-1, 0)] # dy, dx
        random.shuffle(neighbors)
        
        for dx, dy in neighbors:
            nx, ny = cx + dx, cy + dy 
            
            if self._is_valid(nx, ny) and not self.visited[ny, nx]:
                wall_x = mx + dx
                wall_y = my + dy
                
                self.maze[wall_y, wall_x] = self.PATH
                
                self._carve_passages(nx, ny)

    def generate(self):
        start_x = random.randrange(self.logical_width)
        start_y = random.randrange(self.logical_height)
        
        self._carve_passages(start_x, start_y)
        
        return self.maze
