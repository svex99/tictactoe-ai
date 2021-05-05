import random
import json

from src.board import Board


class TTTPlayer:
    """
    Base player of tic tac toe game.
    """
    def __init__(self, symbol):
        self.symbol = symbol

    def choice(self, board: Board):
        """
        Logic of each player.
        Select in board the index for next player move.
        """
        raise NotImplementedError()

    def process_result(self, result: str):
        """
        Proccess the feedback of the enviroment.
        """
        raise NotImplementedError()


class HumanPlayer(TTTPlayer):

    def __init__(self, symbol):
        super().__init__(symbol)

    def choice(self, board: Board):
        print(board)
        next_move = None
        while next_move is None:
            try:
                next_move = int(input('What\'s your next move?: '))
                if next_move not in board.move_options:
                    next_move = None
                    print('Invalid move')
            except ValueError:
                pass

        return next_move

    def process_result(self, result: str):
        if result == self.symbol:
            print(f'{self.symbol} - You won :)')
        elif result == 'draw':
            print(f'{self.symbol} - It\'s a draw :|')
        else:
            print(f'{self.symbol} - You loose :(')


class RandomPlayer(TTTPlayer):
    """
    Player that plays random.
    """
    def __init__(self, symbol):
        super().__init__(symbol)

    def choice(self, board: Board):
        return random.choice(board.move_options)

    def process_result(self, result: str):
        pass


class QPlayer(TTTPlayer):
    """
    Player using Q-Learning algorithm.
    """
    def __init__(self, symbol, states_json=None):
        super().__init__(symbol)
        self.exploratory_rate = 0.1
        self.learning_rate = 0.2
        self.decay_rate = 0.8
        self.states = {}
        self.history = []

        if states_json is not None:
            self._load_from_json(states_json)
            self.exploratory_rate = 0.001

    def choice(self, board: Board):
        options = board.move_options
        current_sate = board.current_state
        exploratory_prob = random.uniform(0, 1)

        if exploratory_prob <= self.exploratory_rate:
            next_move = random.choice(options)
        else:
            max_value = float('-inf')
            next_move = options[0]

            for o in options:
                value = self.states.get((current_sate, o), 0)

                if value > max_value:
                    max_value = value
                    next_move = o

        self.history.append((current_sate, next_move))

        return next_move

    def process_result(self, result: str):
        if result == self.symbol:
            reward = 1
        elif result == 'draw':
            reward = 0.2
        else:
            reward = -1

        for move in reversed(self.history):
            if self.states.get(move) is None:
                self.states[move] = 0

            self.states[move] += \
                self.learning_rate * (reward * self.decay_rate - self.states[move])
            reward = self.states[move]

        self.history = []

    def save_to_json(self, fp):
        states_dict = {}
        for state, action in self.states:
            try:
                states_dict[state][action] = self.states[(state, action)]
            except KeyError:
                states_dict[state] = {action: self.states[(state, action)]}

        with open(fp, 'w', encoding='utf8') as f:
            json.dump(states_dict, f, indent=True)

    def _load_from_json(self, fp):
        with open(fp, encoding='utf8') as f:
            states_dict = json.load(f)

            for state in states_dict:
                for action in states_dict[state]:
                    self.states[(state, int(action))] = states_dict[state][action]
