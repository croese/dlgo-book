import enum
from dlgo.agent import Agent

__all__ = ["MinimaxAgent"]


class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


def find_winning_move(game_state, next_player):
    for candidate_move in game_state.legal_moves(next_player):
        next_state = game_state.apply_move(candidate_move)
        if next_state.is_over() and next_state.winner() == next_player:
            return candidate_move
    return None


def eliminate_losing_moves(game_state, next_player):
    opponent = next_player.other
    possible_moves = []
    for candidate_move in game_state.legal_moves(next_player):
        next_state = game_state.apply_move(candidate_move)
        opponent_winning_move = find_winning_move(next_state, opponent)
        if opponent_winning_move is None:
            possible_moves.append(candidate_move)
    return possible_moves
