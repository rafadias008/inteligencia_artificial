from collections import deque


class PuzzleState:
    def __init__(self, board, parent=None, action=None, cost=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.cost = cost

    def is_goal(self):
        return self.board == (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def get_successors(self):
        successors = []
        zero_idx = self.board.index(0)
        row, col = divmod(zero_idx, 3)
        moves = {'Cima': (-1, 0), 'Baixo': (1, 0), 'Esquerda': (0, -1), 'Direita': (0, 1)}

        for action, (dr, dc) in moves.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                board_list = list(self.board)
                board_list[zero_idx], board_list[new_idx] = board_list[new_idx], board_list[zero_idx]
                new_board = tuple(board_list)
                successors.append(PuzzleState(new_board, self, action, self.cost + 1))

        return successors

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(self.board)

    def display(self):
        """
        Exibe o tabuleiro em formato visual 3x3.
        0 representa o espaço vazio.
        """
        print("┌───┬───┬───┐")
        for i in range(3):
            row = []
            for j in range(3):
                value = self.board[i * 3 + j]
                row.append(f" {value} " if value != 0 else "   ")
            print("│" + "│".join(row) + "│")
            if i < 2:
                print("├───┼───┼───┤")
        print("└───┴───┴───┘")

    def reconstruct_path(self):
        """Reconstrói o caminho da solução"""
        path = []
        current = self
        while current:
            path.append(current.action)
            current = current.parent
        return list(reversed([action for action in path if action]))

    def get_solution_states(self):
        """
        Retorna todos os estados do caminho da solução da raiz até o estado atual.
        Útil para visualizar o progresso passo a passo.
        """
        states = []
        current = self
        while current:
            states.append(current)
            current = current.parent
        return list(reversed(states))


class BuscaEmLargura:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.visited = set()
        self.nodes_expanded = 0

    def search(self):
        """
        Realiza busca em largura (BFS) para encontrar a solução do jogo dos 8.
        Retorna: (solução encontrada, número de nós expandidos, profundidade)
        """
        if self.initial_state.is_goal():
            return self.initial_state.reconstruct_path(), 0, 0

        queue = deque([self.initial_state])
        self.visited.add(self.initial_state.board)
        max_depth = 0

        while queue:
            current_state = queue.popleft()
            self.nodes_expanded += 1

            # Gera sucessores
            for successor in current_state.get_successors():
                if successor.board not in self.visited:
                    if successor.is_goal():
                        path = successor.reconstruct_path()
                        return path, self.nodes_expanded, successor.cost

                    self.visited.add(successor.board)
                    queue.append(successor)
                    max_depth = max(max_depth, successor.cost)

        return None, self.nodes_expanded, max_depth  # Sem solução


# Exemplo de uso
if __name__ == "__main__":
    # Estado inicial (0 representa o espaço vazio)
    initial_board = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    
    initial_state = PuzzleState(initial_board)
    bfs = BuscaEmLargura(initial_state)
    
    print("\n" + "="*40)
    print("JOGO DOS 8 - BUSCA EM LARGURA")
    print("="*40)
    
    print("\n📍 ESTADO INICIAL:")
    initial_state.display()
    
    print("\nIniciando busca em largura...")
    solution, nodes_expanded, depth = bfs.search()
    
    if solution:
        print(f"\n✓ Solução encontrada!")
        print(f"Número de passos: {len(solution)}")
        print(f"Nós expandidos: {nodes_expanded}")
        print(f"Movimentos: {' → '.join(solution)}")
        
        # Reconstrói e exibe todos os passos da solução
        solution_states = initial_state.get_solution_states()
        # A função search() de BuscaEmLargura retorna a solução, mas precisamos dos estados
        # Vamos reconstruir baseado no número de passos
        
        print("\n" + "-"*40)
        print("PASSOS DA SOLUÇÃO:")
        print("-"*40)
        
        current = initial_state
        print(f"\nPasso 0 (Inicial):")
        current.display()
        
        step = 1
        for move in solution:
            # Encontra o sucessor que corresponde ao movimento
            for successor in current.get_successors():
                if successor.action == move:
                    print(f"\nPasso {step}: {move}")
                    successor.display()
                    current = successor
                    step += 1
                    break
        
        print("\n" + "="*40)
        print("🎉 OBJETIVO ATINGIDO!")
        print("="*40 + "\n")
    else:
        print("\n✗ Nenhuma solução encontrada")
        print(f"Nós expandidos: {nodes_expanded}\n")