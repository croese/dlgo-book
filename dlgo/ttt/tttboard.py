import copy
from dlgo.ttt.ttttypes import Player, Point

__all__ = [
    "Board",
    "GameState",
    "Move",
]

BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
# top left to bottom right diagonal
DIAG_1 = (Point(1, 1), Point(2, 2), Point(3, 3))
# top right to bottom left diagonal
DIAG_2 = (Point(1, 3), Point(2, 2), Point(3, 1))


class Move:
    def __init__(self, point: Point) -> None:
        self.point = point


class Board:
    def __init__(self) -> None:
        self._grid = {}

    def place(self, player: Player, point: Point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        self._grid[point] = player

    @staticmethod
    def is_on_grid(point: Point):
        return 1 <= point.row <= BOARD_SIZE and 1 <= point.col <= BOARD_SIZE

    def get(self, point: Point):
        return self._grid.get(point)


class GameState:
    def __init__(self, board: Board, next_player: Player, move: Move) -> None:
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move: Move):
        next_board = copy.deepcopy(self.board)
        next_board.place(self.next_player, move.point)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls):
        board = Board()
        return GameState(board, Player.x, None)

    def is_valid_move(self, move: Move):
        return self.board.get(move.point) is None and not self.is_over()

    def legal_moves(self):
        moves = []
        for row in ROWS:
            for col in COLS:
                move = Move(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        return moves

    def is_over(self):
        if self._has_3_in_a_row(Player.x):
            return True
        if self._has_3_in_a_row(Player.o):
            return True
        if all(
            self.board.get(Point(row, col)) is not None for row in ROWS for col in COLS
        ):
            return True
        return False

    def _has_3_in_a_row(self, player):
        # Vertical
        for col in COLS:
            if all(self.board.get(Point(row, col)) == player for row in ROWS):
                return True
        # Horizontal
        for row in ROWS:
            if all(self.board.get(Point(row, col)) == player for col in COLS):
                return True
        # Diagonal UL to LR
        if all(self.board.get(p) == player for p in DIAG_1):
            return True
        # Diagonal UR to LL
        if all(self.board.get(p) == player for p in DIAG_2):
            return True
        return False

    def winner(self):
        if self._has_3_in_a_row(Player.x):
            return Player.x
        if self._has_3_in_a_row(Player.o):
            return Player.o
        return None
