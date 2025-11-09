import random
import numpy as np
import matplotlib.pyplot as plt

from mazeGen import MazeGenerator
from agente import Agente

def main():
  
    #  define labirinto 
    SEED = 42
    LARGURA = 16
    ALTURA = 16

    #  gera labirinto 
    print(f"Gerando Labirinto {LARGURA}x{ALTURA} (Seed={SEED})")
    gen1 = MazeGenerator(width=LARGURA, height=ALTURA, seed=SEED)
    labirinto = gen1.generate()
  
    START_POS = (1, 1) 
    
    y_indices, x_indices = np.where(labirinto == gen1.PATH)

    # array lista cordenada 
    valid_path_coords = list(zip(y_indices, x_indices)) # rmv inicio lista alvos

    # partida valida se != objetivo
    if START_POS in valid_path_coords:
        valid_path_coords.remove(START_POS)
    random.seed(SEED)

    # escolhe objetivo aleatorio
    GOAL_POS = random.choice(valid_path_coords)

    print(f"Partida: {START_POS}")
    print(f"Objetivo: {GOAL_POS}")

    #  inicia agente
    print(f"Iniciando Agente A* de {START_POS} para {GOAL_POS}")
    agente = Agente(labirinto, START_POS, GOAL_POS)

    #  cfg animacao
    plt.rcParams['toolbar'] = 'None'
    plt.ion() # ativa modo interativo
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # cria img
    img_pb = np.stack([labirinto]*3, axis=-1).astype(float)
    
    # inverte cores caminho branco parede preto
    img_visual_base = 1.0 - img_pb 
    
    img_plot = ax.imshow(img_visual_base, interpolation='nearest')
    
    ax.plot(START_POS[1], START_POS[0], 'bo', markersize=10, label='Início') # circulo azul
    ax.plot(GOAL_POS[1], GOAL_POS[0], 'go', markersize=10, label='Fim')   # circulo verde
    
    ax.set_title(f"(Seed={SEED}) - Buscando...")
    ax.axis('off')
    
    plt.show(block=False) # Mostra a janela
    
    #  loop animacao
    status = "searching"
    current_visual = None
    try:
        while status == "searching":
            status = agente.solve_step()
            
            # prepara img
            current_visual = np.copy(img_visual_base)
            
            # pinta nos explorados
            for (y, x) in agente.explored_nodes:
                if (y, x) != START_POS and (y, x) != GOAL_POS:
                    current_visual[y, x] = [0.7, 0.7, 0.7] # Cinza
            
            img_plot.set_data(current_visual)
            
            fig.canvas.draw_idle()
            plt.pause(0.003)

    except Exception as e:
        print(f"\nSimulação interrompida. {e}")
        plt.ioff()
        return

    #  apresenta caminho 
    if status == "goal_found":
        ax.set_title(f"(Seed={SEED}) - Caminho Encontrado!")
 
        path_y = [p[0] for p in agente.path]
        path_x = [p[1] for p in agente.path]
        
        # Desenha a linha
        ax.plot(path_x, path_y, color='red', linewidth=2, label='Caminho Final') 
        
        fig.canvas.draw_idle()
        
    elif status == "no_path":
        print("\n FALHA ")
        ax.set_title(f"A* (Seed={SEED}) - Sem Caminho!")
        
    print("Simulação concluída. Feche a janela para sair.")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()