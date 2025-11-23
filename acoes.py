import networkx as nx
import matplotlib.pyplot as plt

class VisualizadorAcoes:
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = {}
        
        # define nos
        self.G.add_node("input")
        self.G.add_node("esq")
        self.G.add_node("move")
        self.G.add_node("dir")
        
        # define arestas
        self.G.add_edge("input", "esq")
        self.G.add_edge("input", "move")
        self.G.add_edge("input", "dir")
        
        # layout
        self.pos["input"] = (0.5, 0.55)  
        self.pos["esq"] = (0.3, 0.5)
        self.pos["move"] = (0.5, 0.5)
        self.pos["dir"] = (0.7, 0.5)

    def get_relative_direction(self, p1, p2, p3):
        """Calcula a direcao: Avo(p1) -> Pai(p2) -> Filho(p3)"""
        if not p1 or not p2 or not p3: 
            return "Start"
            
        # vetor anterior
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        # vetor atual
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        
        # se igual move
        if v1 == v2: 
            return "move"
        
        # produto vetorial identificar esq ou dir
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        
        if cross > 0: return "esq"
        elif cross < 0: return "dir"
        else: return "volta"

    def draw(self, ax, p1, p2, p3):
        ax.clear()
        
        # descobre a acao
        action = self.get_relative_direction(p1, p2, p3)
        
        # define cores
        colors = []
        sizes = []
        
        for node in self.G.nodes():
            if node == action:
                colors.append('#00FF00') 
                sizes.append(800)
            elif node == "input":
                colors.append('#AAAAFF')
                sizes.append(800)
            else:
                colors.append('#EEEEEE')
                sizes.append(800)
                
        # desenha arestas
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edge_color='#AAAAAA', 
                             width=2.0, arrows=False)
        
        # desenha nos
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax, node_color=colors, 
                             node_size=sizes, edgecolors='black')
        
        # textos
        nx.draw_networkx_labels(self.G, self.pos, ax=ax, font_size=8)
    
        ax.axis('off')