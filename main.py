import gc
import random
import numpy as np
import matplotlib
try:
    matplotlib.use('TkAgg')
except ImportError:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from mazeGen import MazeGenerator
from agente import Agente
from grafos import visualizadorGrafos
from acoes import VisualizadorAcoes

def main():
  
    # defs labirinto
    SEED = random.randint(0, 1000)
    LARGURA = 16
    ALTURA = 16

    # gera labirinto
    print(f"Gerando Labirinto {LARGURA}x{ALTURA} (Seed={SEED})")
    gen1 = MazeGenerator(width=LARGURA, height=ALTURA, seed=SEED)
    labirinto = gen1.generate()
  
    START_POS = (1, 1) 
    1
    y_indices, x_indices = np.where(labirinto == gen1.PATH)

    # array lista cordenada 
    valid_path_coords = list(zip(y_indices, x_indices)) 

    # partida valida se != objetivo
    if START_POS in valid_path_coords:
        valid_path_coords.remove(START_POS)
    random.seed(SEED)

    # escolhe objetivo aleatorio
    GOAL_POS = random.choice(valid_path_coords)

    print(f"Partida: {START_POS}")
    print(f"Objetivo: {GOAL_POS}")

    # init agente
    print(f"Iniciando Agente A* de {START_POS} para {GOAL_POS}")
    agente = Agente(labirinto, START_POS, GOAL_POS)

    # init visualizadores
    grafo_vis = visualizadorGrafos(labirinto, START_POS, GOAL_POS)
    acao_vis = VisualizadorAcoes()

    # cfg animacao
    plt.rcParams['toolbar'] = 'None'
    plt.ion() # ativa modo interativo
    
    # cria figura 2 subplots
    fig = plt.figure(figsize=(18, 9))
    fig.canvas.manager.window.state('zoomed')
    fig.patch.set_facecolor('white')
    fig.suptitle(f"Simulação - Seed {SEED}", fontsize=16)

    gs = GridSpec(2, 2, width_ratios=[1, 1.5], height_ratios=[5, 1])

    ax_graph = fig.add_subplot(gs[0, 0])  
    ax_action = fig.add_subplot(gs[1, 0]) 
    ax_maze = fig.add_subplot(gs[:, 1])

    ax_graph.axis('off')
    ax_action.axis('off')
    ax_maze.axis('off')

    # cfg labirinto dir
    img_pb = np.stack([labirinto]*3, axis=-1).astype(float)
    img_visual_base = 1.0 - img_pb 
    
    img_plot = ax_maze.imshow(img_visual_base, interpolation='nearest')
    
    ax_maze.plot(START_POS[1], START_POS[0], 'bo', markersize=10, label='Início') 
    ax_maze.plot(GOAL_POS[1], GOAL_POS[0], 'go', markersize=10, label='Fim')   
    
    ax_maze.set_title("Visualização do Ambiente")

    # cfg grafo esq
    grafo_vis.draw_graph(ax_graph, set([START_POS]), [], GOAL_POS, show_all=False)

    # cfg acoes esq baixo
    acao_vis.draw(ax_action, None, None, None)

    plt.show(block=False)
    
    # loop animacao
    status = "searching"
    current_visual = None

    current_node = START_POS
    parent_node = None
    grandparent_node = None
    
    try:
        while status == "searching":
            status = agente.solve_step()

            # identifica nos para acoes
            if agente.came_from:
                current_node, parent_node = list(agente.came_from.items())[-1]
                grandparent_node = agente.came_from.get(parent_node)
            
            # att labirinto
            current_visual = np.copy(img_visual_base)
            
            # pinta explorados
            for (y, x) in agente.explored_nodes:
                if (y, x) != START_POS and (y, x) != GOAL_POS:
                    current_visual[y, x] = [0.7, 0.7, 0.7] # cinza
            
            img_plot.set_data(current_visual)
            
            # att grafo
            grafo_vis.draw_graph(ax_graph, agente.explored_nodes, [], GOAL_POS, show_all=False)

            # att acoes
            acao_vis.draw(ax_action, grandparent_node, parent_node, current_node)

            fig.canvas.draw_idle()
            plt.pause(0.001)

    except Exception as e:
        print(f"\nSimulação interrompida. {e}")
        plt.ioff()
        return

    # resultado
    if status == "goal_found":
        fig.suptitle(f"SUCESSO! Caminho Encontrado (Seed={SEED})", color='green', fontsize=16)
 
        # desenha linha mapa
        path_y = [p[0] for p in agente.path]
        path_x = [p[1] for p in agente.path]
        ax_maze.plot(path_x, path_y, color='red', linewidth=3, label='Caminho Final') 
        
        # desenha grafo
        grafo_vis.draw_graph(ax_graph, agente.explored_nodes, agente.path, GOAL_POS, show_all=True)
        
        fig.canvas.draw_idle()
        
    elif status == "no_path":
        print("\n FALHA ")
        fig.suptitle(f"FALHA - Sem Caminho (Seed={SEED})", color='red', fontsize=16)
        
    print("Simulação concluída.")
    plt.ioff()
    plt.show(block=True)

if __name__ == "__main__":
    main()
    gc.collect() # limpa memoria