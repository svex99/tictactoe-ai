import random
import matplotlib.pyplot as plt

from src.players import TTTPlayer, RandomPlayer, QPlayer, HumanPlayer
from src.board import Board


def play_game(board: Board, player_X: TTTPlayer, player_O: TTTPlayer):
    """
    Simulation of a singular tic tac toe game between two players.
    """
    board.reset_board()
    players = (player_X, player_O)
    next_turn = random.randint(0, 1)    # Choose who starts playing

    while not board.game_result:
        actual_player = players[next_turn]
        choosed = actual_player.choice(board)
        board.make_move(actual_player.symbol, choosed)

        next_turn = (next_turn + 1) % 2

    player_X.process_result(board.game_result)
    player_O.process_result(board.game_result)

    return board.game_result


def bot_vs_bot(type_X: str, type_O: str):
    """
    Simulate 1000 matches of 100 games each.
    """
    player_type = {
        'r': RandomPlayer,
        'q': QPlayer,
    }

    matches = 1000
    games_per_match = 100

    won_X = [0 for _ in range(matches + 1)]
    won_O = [0 for _ in range(matches + 1)]
    draws = [0 for _ in range(matches + 1)]

    board = Board()
    player_X = player_type[type_X]('X')
    player_O = player_type[type_O]('O')

    # Simulate (matches * games_per_match) games
    for i in range(1, matches + 1):
        winnings_X = 0
        winnings_O = 0
        match_draws = 0

        for _ in range(games_per_match):
            result = play_game(board, player_X, player_O)

            if result == 'draw':
                match_draws += 1
            elif result == 'X':
                winnings_X += 1
            else:
                winnings_O += 1

        won_X[i] = won_X[i-1] + winnings_X
        won_O[i] = won_O[i-1] + winnings_O
        draws[i] = draws[i-1] + match_draws

    # Plotting results
    colors = ('r', 'b', 'g')
    labels = (
        f'{player_X.symbol}-{player_X.__class__.__name__}',
        f'{player_O.symbol}-{player_O.__class__.__name__}',
        'Draws',
    )
    values = (won_X, won_O, draws)

    for l, c, v in zip(labels, colors, values):
        plt.plot(list(range(matches + 1)), v, color=c, label=l)

    plt.title(f'Winnings in {matches} matches of {games_per_match} games each.')
    plt.xlabel('Match number')
    plt.ylabel('Total winnings')
    leg = plt.legend(loc='upper center', ncol=3, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)

    plt.show()


def human_game(type_X: str, type_O: str):
    """
    Single game between human vs ia or human vs human
    """
    board = Board()

    if type_X == 'h':
        player_X = HumanPlayer('X')
    else:
        player_X = QPlayer('X', states_json='pre_trained_X.json')

    if type_O == 'h':
        player_O = HumanPlayer('O')
    else:
        player_O = QPlayer('O', states_json='pre_trained_O.json')

    play_game(board, player_X, player_O)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-x', help='Player X type, human(\'h\'), random(\'r\') or q-learning(\'q\')')
    parser.add_argument('-o', help='Player O type, human(\'h\'), random(\'r\') or q-learning(\'q\')')
    args = parser.parse_args()

    if args.x not in ('h', 'r', 'q') or args.o not in ('h', 'r', 'q'):
        print('Invalid arguments. See help with: main.py -h')
    else:
        if 'h' in (args.x, args.o):
            human_game(args.x, args.o)
        else:
            bot_vs_bot(args.x, args.o)
