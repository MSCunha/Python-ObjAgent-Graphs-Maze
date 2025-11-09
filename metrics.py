class SearchMetrics:
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.nodes_explored = 0
        self.path_length = 0
        self.path_cost = 0
        self.success = False
    
    @property
    def execution_time(self):
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    @property
    def branching_factor(self):
        if self.path_length == 0:
            return 0.0
        return self.nodes_explored / self.path_length
    
    def print_report(self, algorithm_name="Algoritmo"):
        print(f"\n┌{'─'*68}┐")
        print(f"│ RELATÓRIO: {algorithm_name:<55}│")
        print(f"├{'─'*68}┤")
        
        if not self.success:
            print(f"│ {'Status:':<30} ✗ CAMINHO NÃO ENCONTRADO{' '*18}│")
            print(f"│ {'Tempo de execução:':<30} {self.execution_time:.6f}s{' '*27}│")
            print(f"└{'─'*68}┘")
            return
        
        print(f"│ {'Status:':<30} ✓ CAMINHO ENCONTRADO{' '*24}│")
        print(f"├{'─'*68}┤")
        print(f"│ {'Tempo de execução:':<30} {self.execution_time:.6f} segundos{' '*17}│")
        print(f"│ {'Nós explorados:':<30} {self.nodes_explored:<37}│")
        print(f"│ {'Comprimento do caminho:':<30} {self.path_length} nós{' '*30}│")
        print(f"│ {'Custo do caminho:':<30} {self.path_cost:<37}│")
        print(f"│ {'Fator de ramificação efetivo:':<30} {self.branching_factor:.2f}{' '*34}│")
        
        if self.path_length > 0:
            efficiency = (self.path_length / self.nodes_explored) * 100
            print(f"│ {'Eficiência (% caminho/explorados):':<30} {efficiency:.2f}%{' '*31}│")
        
        print(f"└{'─'*68}┘")
    
    def to_dict(self):
        return {
            'execution_time': self.execution_time,
            'nodes_explored': self.nodes_explored,
            'path_length': self.path_length,
            'path_cost': self.path_cost,
            'branching_factor': self.branching_factor,
            'success': self.success
        }
    
    def __str__(self):
        status = "✓" if self.success else "✗"
        return (f"SearchMetrics({status} | "
                f"time={self.execution_time:.4f}s, "
                f"explored={self.nodes_explored}, "
                f"length={self.path_length}, "
                f"cost={self.path_cost})")
    
    def __repr__(self):
        return self.__str__()