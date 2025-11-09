import argparse
import random
import time
import json
import sys
from pathlib import Path
import numpy as np

import matplotlib
try:
    matplotlib.use('TkAgg')
except ImportError:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

from agente import MazeSolverAgent
from metrics import SearchMetrics
from visualizer import MazeVisualizer

def parse_args():
    parser = argparse.ArgumentParser(
        description='Busca A* em Labirinto com NetworkX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py --width 20 --height 20
  python main.py --seed 42 --compare
        """
    )
    parser.add_argument('--width', type=int, default=20, help='Largura do labirinto')
    parser.add_argument('--height', type=int, default=20, help='Altura do labirinto')
    parser.add_argument('--seed', type=int, default=None, help='Seed para reprodutibilidade')
    parser.add_argument('--animate', action='store_true', help='Ativar animação')
    parser.add_argument('--no-animate', dest='animate', action='store_false', help='Desativar animação')
    parser.add_argument('--animation-speed', type=float, default=0.003, help='Velocidade da animação (s)')
    parser.add_argument('--compare', action='store_true', help='Comparar algoritmos')
    parser.add_argument('--save-results', action='store_true', default=True, help='Salvar resultados em JSON')
    parser.add_argument('--output-dir', type=str, default='results', help='Diretório de saída')
    parser.set_defaults(animate=True)
    return parser.parse_args()

def save_results_to_file(agent_results, args, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = f"maze_{args.width}x{args.height}_seed{args.seed}_{timestamp}"
    
    def convert_to_native(obj):
        if isinstance(obj, np.integer): return int(obj)
        elif isinstance(obj, np.floating): return float(obj)
        elif isinstance(obj, np.ndarray): return obj.tolist()
        elif isinstance(obj, tuple): return [convert_to_native(item) for item in obj]
        elif isinstance(obj, list): return [convert_to_native(item) for item in obj]
        elif isinstance(obj, dict): return {key: convert_to_native(val) for key, val in obj.items()}
        return obj
    
    data = {
        'config': {'width': args.width, 'height': args.height, 'seed': args.seed},
        'start': list(agent_results['start']),
        'goal': list(agent_results['goal']),
        'algorithms': {}
    }
    
    for algo_name, algo_data in agent_results['algorithms'].items():
        metrics = algo_data['metrics']
        data['algorithms'][algo_name] = {
            'success': bool(metrics.success),
            'path_length': int(metrics.path_length),
            'nodes_explored': int(metrics.nodes_explored),
            'execution_time': float(metrics.execution_time),
            'path_cost': float(metrics.path_cost)
        }
    
    json_path = output_path / f"{base_name}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(convert_to_native(data), f, indent=2)
    
    print(f"\n✓ Resultados salvos em: {json_path}")
    return str(output_path / base_name)

def main():
    args = parse_args()
    
    print("="*70)
    print(" BUSCA A* EM LABIRINTO COM NETWORKX".center(70))
    print("="*70)
    
    if args.seed is None:
        args.seed = random.randint(0, 999999)
        print(f"→ Seed gerada automaticamente: {args.seed}")

    try:
        agent = MazeSolverAgent(args.width, args.height, args.seed)
        agent.initialize_environment()

        print(f"\n{'='*70}")
        print(" EXECUTANDO BUSCA PRINCIPAL (A*)".center(70))
        print(f"{'='*70}")
        astar_result = agent.solve_astar()
        astar_result['metrics'].print_report("A*")

        if args.compare:
            print(f"\n{'='*70}")
            print(" COMPARANDO ALGORITMOS".center(70))
            print(f"{'='*70}")
            comparison_results = agent.compare_algorithms()
            for name, data in comparison_results.items():
                if name != 'A*': 
                    data['metrics'].print_report(name)
            agent.print_comparison_table(comparison_results)

        print(f"\n{'='*70}")
        print(" VISUALIZAÇÃO".center(70))
        print(f"{'='*70}")
        
        visualizer = MazeVisualizer(agent.maze, agent.graph, agent.start_pos, agent.goal_pos)

        if args.animate:
            print("\n→ Iniciando animação da busca A*...")
            frames = visualizer.animate_search(
                astar_result['explored'],
                astar_result['path'],
                speed=args.animation_speed
            )

        print("\n→ Gerando imagem final dos resultados...")
        if args.compare and len(agent.results['algorithms']) > 1:
             fig_path = visualizer.visualize_comparison(agent.results['algorithms'])
        else:
             fig_path = visualizer.visualize_final(astar_result['explored'], astar_result['path'])

        if args.save_results:
            base_name = save_results_to_file(agent.results, args, args.output_dir)
            if fig_path:
                import shutil
                final_png = f"{base_name}.png"
                shutil.move(fig_path, final_png)
                print(f"✓ Imagem salva em: {final_png}")

        print(f"\n{'='*70}")
        print(" CONCLUÍDO COM SUCESSO".center(70))
        print(f"{'='*70}")
        print("Feche a janela da visualização para encerrar.")
        plt.show()

    except Exception as e:
        print(f"\n✗ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except KeyboardInterrupt:
        print("\n\n! Interrompido pelo usuário.")
        return 130

    return 0

if __name__ == "__main__":
    sys.exit(main())