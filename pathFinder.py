import time
import networkx as nx
from metrics import SearchMetrics


class PathFinder:
    
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        
        if start not in graph.nodes():
            raise ValueError(f"Nó inicial {start} não existe no grafo")
        if goal not in graph.nodes():
            raise ValueError(f"Nó objetivo {goal} não existe no grafo")
    
    def manhattan_heuristic(self, n1, n2):
        return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])
    
    def run_astar(self):
        metrics = SearchMetrics()
        metrics.start_time = time.time()
        
        try:
            path = nx.astar_path(
                self.graph,
                self.start,
                self.goal,
                heuristic=self.manhattan_heuristic,
                weight='weight'
            )
            
            path_cost = sum(
                self.graph[path[i]][path[i+1]]['weight'] 
                for i in range(len(path)-1)
            )
            explored = self._estimate_explored_nodes(path)
            
            metrics.end_time = time.time()
            metrics.path_length = len(path)
            metrics.path_cost = path_cost
            metrics.nodes_explored = len(explored)
            metrics.success = True
            
            return {
                'path': path,
                'explored': explored,
                'metrics': metrics
            }
            
        except nx.NetworkXNoPath:
            metrics.end_time = time.time()
            metrics.success = False
            return {
                'path': [],
                'explored': set(),
                'metrics': metrics
            }
    
    def run_dijkstra(self):
        metrics = SearchMetrics()
        metrics.start_time = time.time()
        
        try:
            path = nx.dijkstra_path(self.graph, self.start, self.goal, weight='weight')
            path_cost = nx.dijkstra_path_length(self.graph, self.start, self.goal, weight='weight')
            
            explored = self._estimate_explored_nodes(path, algorithm='dijkstra')
            
            metrics.end_time = time.time()
            metrics.path_length = len(path)
            metrics.path_cost = path_cost
            metrics.nodes_explored = len(explored)
            metrics.success = True
            
            return {
                'path': path,
                'explored': explored,
                'metrics': metrics
            }
            
        except nx.NetworkXNoPath:
            metrics.end_time = time.time()
            metrics.success = False
            return {'path': [], 'explored': set(), 'metrics': metrics}
    
    def run_bfs(self):
        metrics = SearchMetrics()
        metrics.start_time = time.time()
        
        try:
            path = nx.shortest_path(self.graph, self.start, self.goal, method='bfs')
            path_cost = len(path) - 1  # BFS não considera pesos
            
            explored = self._estimate_explored_nodes(path, algorithm='bfs')
            
            metrics.end_time = time.time()
            metrics.path_length = len(path)
            metrics.path_cost = path_cost
            metrics.nodes_explored = len(explored)
            metrics.success = True
            
            return {
                'path': path,
                'explored': explored,
                'metrics': metrics
            }
            
        except nx.NetworkXNoPath:
            metrics.end_time = time.time()
            metrics.success = False
            return {'path': [], 'explored': set(), 'metrics': metrics}
    
    def run_dfs(self):
        metrics = SearchMetrics()
        metrics.start_time = time.time()
        
        try:
            path = list(nx.dfs_preorder_nodes(self.graph, self.start))
            
            if self.goal in path:
                goal_idx = path.index(self.goal)
                path = path[:goal_idx+1]
                
                actual_path = nx.shortest_path(self.graph, self.start, self.goal)
                path_cost = len(actual_path) - 1
                
                explored = set(path)
                
                metrics.end_time = time.time()
                metrics.path_length = len(actual_path)
                metrics.path_cost = path_cost
                metrics.nodes_explored = len(explored)
                metrics.success = True
                
                return {
                    'path': actual_path,
                    'explored': explored,
                    'metrics': metrics
                }
            else:
                raise nx.NetworkXNoPath()
                
        except nx.NetworkXNoPath:
            metrics.end_time = time.time()
            metrics.success = False
            return {'path': [], 'explored': set(), 'metrics': metrics}
    
    def _estimate_explored_nodes(self, path, algorithm='astar'):
        explored = set()
        
        for node in path:
            explored.add(node)
            
            if algorithm == 'astar':
                for neighbor in self.graph.neighbors(node):
                    if self.manhattan_heuristic(neighbor, self.goal) <= \
                       self.manhattan_heuristic(node, self.goal):
                        explored.add(neighbor)
            elif algorithm == 'dijkstra':
                for neighbor in self.graph.neighbors(node):
                    explored.add(neighbor)
            elif algorithm == 'bfs':
                for neighbor in self.graph.neighbors(node):
                    explored.add(neighbor)
        
        return explored
    
    def compare_algorithms(self):
        algorithms = {
            'A*': self.run_astar,
            'Dijkstra': self.run_dijkstra,
            'BFS': self.run_bfs,
            'DFS': self.run_dfs
        }
        
        results = {}
        
        for name, algo_func in algorithms.items():
            print(f"\n→ Executando {name}...")
            try:
                result = algo_func()
                results[name] = result
                
                if result['metrics'].success:
                    print(f"  ✓ Caminho encontrado: {result['metrics'].path_length} passos")
                else:
                    print(f"  ✗ Caminho não encontrado")
                    
            except Exception as e:
                print(f"  ✗ Erro ao executar {name}: {e}")
                metrics = SearchMetrics()
                metrics.success = False
                results[name] = {'path': [], 'explored': set(), 'metrics': metrics}
        
        return results
    
    def print_comparison_table(self, results):
        print(f"\n{'='*90}")
        print(" TABELA COMPARATIVA DE ALGORITMOS".center(90))
        print(f"{'='*90}")
        
        header = f"{'Algoritmo':<12} | {'Tempo (s)':<10} | {'Nós Exp.':<10} | " \
                 f"{'Tamanho':<10} | {'Custo':<10} | {'Status':<10}"
        print(header)
        print("-" * 90)
        
        for algo_name, result in results.items():
            m = result['metrics']
            
            status = "✓ OK" if m.success else "✗ FALHA"
            tempo = f"{m.execution_time:.4f}" if m.success else "N/A"
            nodes = str(m.nodes_explored) if m.success else "N/A"
            length = str(m.path_length) if m.success else "N/A"
            cost = str(m.path_cost) if m.success else "N/A"
            
            row = f"{algo_name:<12} | {tempo:<10} | {nodes:<10} | " \
                  f"{length:<10} | {cost:<10} | {status:<10}"
            print(row)
        
        print("=" * 90)
        
        successful = {name: res for name, res in results.items() 
                     if res['metrics'].success}
        
        if successful:
            fastest = min(successful.items(), 
                         key=lambda x: x[1]['metrics'].execution_time)
            least_explored = min(successful.items(), 
                                key=lambda x: x[1]['metrics'].nodes_explored)
            
            print(f"\n🏆 Mais rápido: {fastest[0]} ({fastest[1]['metrics'].execution_time:.4f}s)")
            print(f"🎯 Menos nós explorados: {least_explored[0]} ({least_explored[1]['metrics'].nodes_explored} nós)")