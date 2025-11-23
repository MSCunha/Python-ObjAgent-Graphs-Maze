import networkx as nx
import matplotlib.pyplot as plt

class visualizadorGrafos:
    def __init__(self, maze_matrix, start_pos, goal_pos):
        self.maze = maze_matrix
        self.start = start_pos
        self.goal = goal_pos
        self.PATH = 0
        
        # Grafo
        self.full_grid_graph = nx.Graph()
        self._build_grid_graph()
        
        # arvore completa
        if len(self.full_grid_graph) > 0:
            self.full_tree = nx.bfs_tree(self.full_grid_graph, source=self.start)
        else:
            self.full_tree = nx.DiGraph()
            self.full_tree.add_node(self.start)

        # arvore resumida
        self.display_tree = nx.DiGraph()
        self.dummy_nodes = set() 
        self._build_compressed_tree()

        self.pos = self._layout_arvore(self.display_tree, root=self.start)

    def _build_grid_graph(self):
        h, w = self.maze.shape
        for y in range(h):
            for x in range(w):
                if self.maze[y, x] == self.PATH:
                    node = (y, x)
                    self.full_grid_graph.add_node(node)
                    if x+1 < w and self.maze[y, x+1] == self.PATH:
                        self.full_grid_graph.add_edge(node, (y, x+1))
                    if y+1 < h and self.maze[y+1, x] == self.PATH:
                        self.full_grid_graph.add_edge(node, (y+1, x))

    def _build_compressed_tree(self):
        queue = [self.start]
        visited = {self.start}
        self.display_tree.add_node(self.start)
        
        while queue:
            curr = queue.pop(0)
            children = []
            if curr in self.full_tree:
                children = list(self.full_tree.successors(curr))

            for child in children:
                temp = child
                path_segment = [temp]
                
                # avanca reta
                while True:
                    #se no objetivo para
                    if temp == self.goal:
                        break

                    successors = list(self.full_tree.successors(temp))
                    if len(successors) != 1: 
                        break

                    next_node = successors[0]

                    # avanca se proximo = objetivo
                    if next_node == self.goal:
                        temp = next_node
                        path_segment.append(temp)
                        break

                    temp = successors[0]
                    path_segment.append(temp)

                target = temp 
                
                # Se segmento longo cria substituto
                if len(path_segment) > 2:
                    dummy = f"cut_{curr}_{target}"
                    self.dummy_nodes.add(dummy)
                    
                    self.display_tree.add_node(dummy)
                    self.display_tree.add_node(target)
                    self.display_tree.add_edge(curr, dummy)
                    self.display_tree.add_edge(dummy, target)
                else:
                    self.display_tree.add_node(target)
                    self.display_tree.add_edge(curr, target)

                if target not in visited:
                    visited.add(target)
                    queue.append(target)

    def _layout_arvore(self, G, root=None):
        """Calcula posições X, Y para desenhar a arvore bonita"""
        pos = {}
        width = {}

        if root not in G: return nx.spring_layout(G)

        # largura de cada sub arvore
        def get_width(node):
            children = list(G.successors(node))
            if not children:
                width[node] = 1.0
                return 1.0
            w = sum(get_width(c) for c in children) + (len(children)-1)*2.0
            width[node] = w
            return w
        
        get_width(root)

        # Posicao X Y
        def set_pos(node, left, y):
            children = list(G.successors(node))
            
            if not children:
                pos[node] = (left + width[node]/2, y)
                return
            
            curr_x = left
            child_x = []
            for child in children:
                set_pos(child, curr_x, y - 6.0)
                child_x.append(pos[child][0])
                curr_x += width[child] + 2.0
            
            center = sum(child_x) / len(child_x)
            pos[node] = (center, y)

        set_pos(root, 0, 0)
        return pos

    def draw_graph(self, ax, explored, path, goal, show_all=False, came_from=None):
        ax.clear()
        
        # desenha arvore ref
        nx.draw_networkx_edges(self.display_tree, self.pos, ax=ax, 
                             edge_color="#8B8B8B", arrows=False)
        
        # nao desenha dummy nodes (retos)
        unvisited = [n for n in self.display_tree.nodes() 
                    if n not in explored and n not in self.dummy_nodes]
        
        nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, 
                             nodelist=unvisited,
                             node_color="white", node_size=35, edgecolors="#8B8B8B")
        
        # nos para desenhar
        active = []
        path_nodes = []
        
        # se caminho
        dummy_path = set()
        
        for node in self.display_tree.nodes():
            if node == self.start or node == goal: continue

            if node in self.dummy_nodes:
                # pinta linha vermelha mas nao add node
                preds = list(self.display_tree.predecessors(node))
                if preds and preds[0] in explored:
                    succs = list(self.display_tree.successors(node))
                    if path and preds[0] in path and succs and succs[0] in path:
                        dummy_path.add(node)
            
            elif node in path:
                path_nodes.append(node)
            elif node in explored:
                active.append(node)

        # explorados
        edges_active = []
        for u, v in self.display_tree.edges():
            u_ok = (u in explored) or (u in self.dummy_nodes) or (u == self.start)
            v_ok = (v in explored) or (v in self.dummy_nodes)
            
            # se pai visitado desenha linha
            if u in explored or u in self.dummy_nodes:
                 if v in self.dummy_nodes:
                     ps = list(self.display_tree.predecessors(v))
                     if ps and ps[0] in explored: edges_active.append((u,v))
                 elif v in explored:
                     edges_active.append((u,v))

        nx.draw_networkx_edges(self.display_tree, self.pos, ax=ax, edgelist=edges_active,
                             edge_color='#646464', width=2.5, arrows=False)
        
        # caminho
        edges_path = []
        if path:
            for u, v in self.display_tree.edges():
                u_ok = (u in path) or (u in dummy_path) or (u == self.start)
                v_ok = (v in path) or (v in dummy_path) or (v == goal)
                if u_ok and v_ok: edges_path.append((u,v))
                    
        nx.draw_networkx_edges(self.display_tree, self.pos, ax=ax, edgelist=edges_path,
                             edge_color='#FF4444', width=2.5, arrows=False)

        # explorados
        nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, nodelist=active,
                             node_color='black', node_size=80, edgecolors="black")
        
        # caminho
        nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, nodelist=path_nodes,
                             node_color='#FF4444', node_size=100, edgecolors='#8B0000')

        # inicio
        nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, nodelist=[self.start],
                             node_color='#4444FF', node_size=130, edgecolors='black')
        
        # fim
        goal_list = [goal] if goal in explored or show_all else []
        nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, nodelist=goal_list,
                             node_color='#44FF44', node_size=130, edgecolors='black')

        if goal in self.display_tree:
            nx.draw_networkx_nodes(self.display_tree, self.pos, ax=ax, nodelist=[goal],
                                 node_color='#44FF44', node_size=150, edgecolors='black')

        ax.set_title(f"Nos Visitados: {len(explored)}", fontsize=12)