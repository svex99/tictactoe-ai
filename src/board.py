class Board:

    def __init__(self):
        self.board = None
        self.game_result = None     # May be: 'draw', 'X' or 'O'
        self.reset_board()
        self.winning_combs = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )

    def reset_board(self):
        self.board = [' '] * 9
        self.game_result = None

    def make_move(self, p_symbol, index):
        assert self.board[index] == ' '
        self.board[index] = p_symbol

        # Decide if this play defined the game result
        if any([all([self.board[i] == p_symbol for i in comb]) for comb in self.winning_combs]):
            self.game_result = p_symbol
        elif not self.move_options:
            self.game_result = 'draw'

        return self.game_result

    @property
    def move_options(self):
        return [i for i in range(len(self.board)) if self.board[i] == ' ']

    @property
    def current_state(self):
        return ''.join(c for c in self.board)

    def __repr__(self):
        b = self.board
        return (
            f' {b[0]} | {b[1]} | {b[2]} \n'
            '---+---+---\n'
            f' {b[3]} | {b[4]} | {b[5]} \n'
            '---+---+---\n'
            f' {b[6]} | {b[7]} | {b[8]} '
        )
