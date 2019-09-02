"""
    The connect Z game module
"""
from connectz_engine.player import Player
from contracts.outputs import GameOutputs

from connectz_engine.player import PlayerWin


class IllegalGameSpecError(BaseException):
    pass


class IllegalColumnError(BaseException):
    pass


class IllegalRowError(BaseException):
    pass


class IllegalContinue(BaseException):
    pass


class Draw(BaseException):
    pass


class Neighbours:
    NORTH_WEST = (-1, -1)
    WEST = (0, -1)
    SOUTH_WEST = (1, -1)
    SOUTH = (-1, 0)
    SOUTH_EAST = (-1, 1)
    EAST = (0, 1)
    NORTH_EAST = (1, 1)


class ConnectZGame:

    def __init__(self, game_specs):
        self._cols, self._rows, self._connects = game_specs
        self._check_game_size()  # check the game size
        self._player1 = True  # the player that start the game
        self._game_bed = [[None] * self._cols for _ in range(self._rows)]  # Game bed, saving position of players
        self._row_tracker = [self._rows] * self._cols  # row tracker, how many drops on each column
        self._game_status = None  # current game status

    def _check_game_size(self):
        if self._connects > max(self._cols, self._rows):  # not a valid game spec
            raise IllegalGameSpecError  # raise exception

    def _get_player(self, row_col, offset=(0, 0), player1=True):
        """
        A function to help accessing neighbours
        :param row_col: Tuple(row, col)
        :param offset: Direction
        :param player1: Just choose same player
        :return: A valid neighbour otherwise None
        """
        row_col = (row_col[0] - offset[0], row_col[1] - offset[1])
        if min(row_col) < 0:
            return None

        if row_col[0] >= self._rows:
            return None

        if row_col[1] >= self._cols:
            return None

        neighbour = self._game_bed[row_col[0]][row_col[1]]
        if neighbour is not None:
            if neighbour.player1 == player1:  # only return friends
                return neighbour

    def _find_all_neighbours(self, player: Player):
        """
        Finding all neighbours of the new player
        :param player: New player object
        :return: vertical, horizontal and diagonal friends only
        """
        row_col = player.row_col
        player1 = player.player1

        ver_neighbours = []
        hor_neighbours = []
        diag_neighbours = []

        # horizontal neighbours
        hor_neighbours.append(self._get_player(row_col, Neighbours.EAST, player1))
        hor_neighbours.append(self._get_player(row_col, Neighbours.WEST, player1))

        # vertical neighbours
        ver_neighbours.append(self._get_player(row_col, Neighbours.SOUTH, player1))

        # Diagonal neighbours
        diag_neighbours.append(self._get_player(row_col, Neighbours.NORTH_WEST, player1))
        diag_neighbours.append(self._get_player(row_col, Neighbours.SOUTH_WEST, player1))
        diag_neighbours.append(self._get_player(row_col, Neighbours.NORTH_EAST, player1))
        diag_neighbours.append(self._get_player(row_col, Neighbours.SOUTH_EAST, player1))

        # getting rid of None elements, was easier to have loads of if else
        ver_neighbours = [n for n in ver_neighbours if n is not None]
        hor_neighbours = [n for n in hor_neighbours if n is not None]
        diag_neighbours = [n for n in diag_neighbours if n is not None]

        return ver_neighbours, hor_neighbours, diag_neighbours

    def _create_join_merge_groups(self, player, neighbours):
        """
        This function, create, join and merge groups
        :param player: new player
        :param neighbours: all friend neighbours around
        :return: None
        """
        new_vert_groups = []
        new_hori_groups = []
        new_diag_groups = []
        v_neighbours,  h_neighbours, d_neighbours = neighbours
        if v_neighbours:  # if it is not empty
            for soldier in v_neighbours:
                if soldier.vertical_join(player) is None:  # unable to join their group, I need to create my own group
                    new_vert_groups.append(soldier)

        if h_neighbours:
            for soldier in h_neighbours:
                if soldier.horizontal_join(player) is None:  # unable to join horizontal friends, need to create group
                    new_hori_groups.append(soldier)

        if d_neighbours:
            for soldier in d_neighbours:
                if soldier.diagonal_join(player) is None:  # unable to join diagonal friend, need to create new group
                    new_diag_groups.append(soldier)

        for friend in new_vert_groups:  # let's try creating a new group with vertical friends
            player.create_vertical_group_with(friend)

        for friend in new_hori_groups: # let's try creating a new group with horizontal friends
            player.create_horizontal_group_with(friend)

        for friend in new_diag_groups: # let's try creating a new group with diagonal friends
            player.create_diagonal_group_with(friend)

    def drop(self, col):
        """
        Drop coin function
        :param col: the column that drop will happen on
        :return: Game status
        """
        if self._game_status == GameOutputs.PLAYER1_WIN or \
                self._game_status == GameOutputs.PLAYER2_WIN or self._game_status == GameOutputs.DRAW:
            raise IllegalContinue  # if game has already have a winner or draw

        if col >= self._cols:  # wrong column
            raise IllegalColumnError

        self._row_tracker[col] -= 1  # update the select column row number
        row = self._row_tracker[col]  # selected row

        if row < 0:  # out of game space
            raise IllegalRowError

        new_player = Player(row, col, self._player1, self._connects)  # creating a new soldier, player
        self._game_bed[row][col] = new_player  # sitting the soldier on the board

        try:
            self._create_join_merge_groups(new_player, self._find_all_neighbours(new_player))  # let's find and join
            # friends or creating a new group with them
        except Draw:
            self._game_status = GameOutputs.DRAW
        except PlayerWin:
            self._game_status = GameOutputs.PLAYER1_WIN if self._player1 else GameOutputs.PLAYER2_WIN

        self._player1 = not self._player1  # Toggle player

        if self._game_status != GameOutputs.PLAYER1_WIN and self._game_status != GameOutputs.PLAYER2_WIN:
            if sum(self._row_tracker) == 0:  # All columns filled
                self._game_status = GameOutputs.DRAW
            else:  # still some empty columns to play
                self._game_status = GameOutputs.INCOMPLETE

        return self._game_status

    def print_game_board(self):
        for row in self._game_bed:
            for col in row:
                if col is not None:
                    print(str(col), '| ', end='')
                else:
                    print('  | ', end='')
            print('')
