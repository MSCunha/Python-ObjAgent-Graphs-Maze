import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import io


class MazeVisualizer:
    
    def __init__(self, maze, graph, start, goal):
        self.maze = maze
        self.graph = graph
        self.start = start
        self.goal = goal

        img_pb = np.stack([maze]*3, axis=-1).astype(float)
        self.img_base = 1.0 - img_pb 
    
    def animate_search(self, explored_nodes, final_path, speed=0.003):
        plt.rcParams['toolbar'] = 'None'
        plt.ion()
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Configuração inicial
        img_plot = ax.imshow(self.img_base, interpolation='nearest')
        ax.plot(self.start[1], self.start[0], 'bo', markersize=12, 
                label='Início', markeredgecolor='white', markeredgewidth=1.5)
        ax.plot(self.goal[1], self.goal[0], 'go', markersize=12, 
                label='Objetivo', markeredgecolor='white', markeredgewidth=1.5)
        ax.set_title("Busca A* - Explorando...", fontsize=16, fontweight='bold')
        ax.axis('off')
        ax.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        plt.show(block=False)
        
        frames = []
        
        explored_list = list(explored_nodes)
        
        for i, node in enumerate(explored_list):
            current_visual = np.copy(self.img_base)
            
            for explored_node in explored_list[:i+1]:
                y, x = explored_node
                if explored_node != self.start and explored_node != self.goal:
                    current_visual[y, x] = [0.85, 0.85, 0.95]  # Azul claro
            
            img_plot.set_data(current_visual)
            ax.set_title(f"Busca A* - Explorando... ({i+1}/{len(explored_list)} nós)", 
                        fontsize=16, fontweight='bold')
            
            fig.canvas.draw_idle()
            plt.pause(speed)
            
            if i % 5 == 0:
                frames.append(self._capture_frame(fig))
        
        if final_path:
            current_visual = np.copy(self.img_base)
            
            for node in explored_nodes:
                y, x = node
                if node != self.start and node != self.goal:
                    current_visual[y, x] = [0.85, 0.85, 0.95]
            
            img_plot.set_data(current_visual)
            
            # Desenha caminho
            path_y = [p[0] for p in final_path]
            path_x = [p[1] for p in final_path]
            ax.plot(path_x, path_y, color='red', linewidth=3, 
                   label='Caminho Final', zorder=10)
            
            ax.set_title(f"✓ Caminho Encontrado! ({len(final_path)} passos)", 
                        fontsize=16, fontweight='bold', color='green')
            ax.legend(loc='upper right', fontsize=10)
            
            fig.canvas.draw_idle()
            
            frames.append(self._capture_frame(fig))
        
        plt.ioff()
        return frames
    
    def visualize_final(self, explored_nodes, path):
        fig, ax = plt.subplots(figsize=(12, 12))
        

        img_colored = np.copy(self.img_base)

        for node in explored_nodes:
            y, x = node
            if node != self.start and node != self.goal and node not in path:
                img_colored[y, x] = [0.85, 0.85, 0.95]
        
        for node in path:
            y, x = node
            if node != self.start and node != self.goal:
                img_colored[y, x] = [1.0, 0.8, 0.8] 
        
        ax.imshow(img_colored, interpolation='nearest')
        
        if path:
            path_y = [p[0] for p in path]
            path_x = [p[1] for p in path]
            ax.plot(path_x, path_y, color='red', linewidth=3, 
                   label=f'Caminho ({len(path)} passos)', zorder=10)
        
        ax.plot(self.start[1], self.start[0], 'bo', markersize=15, 
                label='Início', markeredgecolor='white', markeredgewidth=2, zorder=11)
        ax.plot(self.goal[1], self.goal[0], 'go', markersize=15, 
                label='Objetivo', markeredgecolor='white', markeredgewidth=2, zorder=11)
        
        ax.set_title(f"Resultado A* - Caminho Encontrado", 
                    fontsize=18, fontweight='bold')
        ax.axis('off')
        ax.legend(loc='upper right', fontsize=12)
        
        plt.tight_layout()
        
        temp_path = 'temp_visualization.png'
        plt.savefig(temp_path, dpi=150, bbox_inches='tight')
        
        return temp_path
    
    def visualize_comparison(self, algorithms_results):
        num_algos = len(algorithms_results)
        fig, axes = plt.subplots(1, num_algos, figsize=(6*num_algos, 6))
        
        if num_algos == 1:
            axes = [axes]
        
        for idx, (algo_name, result) in enumerate(algorithms_results.items()):
            ax = axes[idx]
            
            img_colored = np.copy(self.img_base)
            
            for node in result['explored']:
                y, x = node
                if node != self.start and node != self.goal and node not in result['path']:
                    img_colored[y, x] = [0.85, 0.85, 0.95]
            
            for node in result['path']:
                y, x = node
                if node != self.start and node != self.goal:
                    img_colored[y, x] = [1.0, 0.8, 0.8]
            
            ax.imshow(img_colored, interpolation='nearest')
            
            if result['path']:
                path_y = [p[0] for p in result['path']]
                path_x = [p[1] for p in result['path']]
                ax.plot(path_x, path_y, color='red', linewidth=2, zorder=10)
            
            ax.plot(self.start[1], self.start[0], 'bo', markersize=10, zorder=11)
            ax.plot(self.goal[1], self.goal[0], 'go', markersize=10, zorder=11)
            
            m = result['metrics']
            title = f"{algo_name}\n"
            if m.success:
                title += f"Passos: {m.path_length} | Explorados: {m.nodes_explored}\n"
                title += f"Tempo: {m.execution_time:.4f}s"
            else:
                title += "Caminho não encontrado"
            
            ax.set_title(title, fontsize=10, fontweight='bold')
            ax.axis('off')
        
        plt.suptitle("Comparação de Algoritmos", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        temp_path = 'temp_comparison.png'
        plt.savefig(temp_path, dpi=150, bbox_inches='tight')
        
        return temp_path
    
    def _capture_frame(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf).copy()
        buf.close()
        return img