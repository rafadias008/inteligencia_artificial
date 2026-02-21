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