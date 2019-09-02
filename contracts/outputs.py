from enum import IntEnum, unique

@unique
class GameOutputs(IntEnum):
    DRAW = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    INCOMPLETE = 3
    ILLEGAL_CONTINUE = 4
    ILLEGAL_ROW = 5
    ILLEGAL_COL = 6
    ILLEGAL_GAME = 7
    INVALID_FILE = 8
    FILE_ERROR = 9
