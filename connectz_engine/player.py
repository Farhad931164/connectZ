from enum import Enum, unique, auto


class PlayerWin(BaseException):
    pass


@unique
class GroupPosition(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()
    SW_NE_DIAGONAL = auto()
    SE_NW_DIAGONAL = auto


class Group:
    def __init__(self, start, end, type_: GroupPosition, connects):
        self._start = start
        self._end = end
        self._connects = connects

        if GroupPosition == GroupPosition.VERTICAL:
            if start.position[1] > end.position[1]:  # if starting column is more than end column, need to reconsider later
                self._start = end
                self._end = start

        self._type = type_
        self._members = [start, end]
        self.check_distance()

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def group_type(self):
        return self._type

    def check_distance(self):
        dist = abs(self.start.position[0] - self.end.position[0]) + \
               abs(self.start.position[1] - self.end.position[1])

        if self._type == GroupPosition.HORIZONTAL or self._type == GroupPosition.VERTICAL:
            dist += 1
        print(f"dist: {dist}")
        if dist >= self._connects:
            raise PlayerWin

    def set_members(self, members):
        self._members.clear()
        self._members.append(members)

    def change_group(self, new_group):
        for member in self._members:
            member.set_group(new_group, self._type)

        new_group.set_members(self._members)

    def update(self, new_member):
        self._members.append(new_member)
        if self._type == GroupPosition.VERTICAL:
            self._end = new_member
        else:
            if new_member.position[1] < self._start.position[1]:
                _start = new_member
            else:
                _end = new_member

        self.check_distance()


class Player:
    def __init__(self, row, col, player1, connects):
        self._player1 = player1
        self._groups = {k: None for k in GroupPosition}
        self._col = col
        self._row = row
        self._connects = connects

    def get_group(self, position: GroupPosition):
        return self._groups[position]

    def set_group(self, group, position: GroupPosition):
        self._groups[position] = group

    @property
    def player1(self):
        return self._player1

    @property
    def row_col(self):
        return self._row, self._col

    @property
    def position(self):
        return self.row_col

    def vertical_join(self, guest):
        vert_group = self.get_group(GroupPosition.VERTICAL)
        if vert_group is None:  # there is no vertical group
            return None
        else:
            vert_group.update(guest)
            guest.set_group(vert_group, GroupPosition.VERTICAL)
            return vert_group

    def horizontal_join(self, guest):
        hori_group = self.get_group(GroupPosition.HORIZONTAL)
        if hori_group is None:
            return None
        else:
            hori_group.update(guest)
            guest_horizontal_group = guest.get_group(GroupPosition.HORIZONTAL)
            if guest_horizontal_group is None:
                guest.set_group(hori_group, GroupPosition.HORIZONTAL)
            else:  # group merge required
                self._merge_groups(guest_horizontal_group, self.get_group(GroupPosition.HORIZONTAL))

            return hori_group

    def _merge_groups(self, group1: Group, group2: Group):
        if group1.group_type == GroupPosition.HORIZONTAL and group2.group_type == GroupPosition.HORIZONTAL:
            if group1.start.position[1] < group2.start.position[1]:
                new_start = group1.start
                new_end = group2.end
            else:
                new_start = group2.start
                new_end = group1.end

            new_group = Group(new_start, new_end, GroupPosition.HORIZONTAL, self._connects)
            group1.change_group(new_group)
            group2.change_group(new_group)

        if group1.group_type == GroupPosition.SW_NE_DIAGONAL or group1.group_type == GroupPosition.SE_NW_DIAGONAL:
            if group1.start.position[0] < group2.start.position[0]:
                new_start = group1.start
                new_end = group2.end
            else:
                new_start = group2.start
                new_end = group1.end

            new_group = Group(new_start, new_end, group1.group_type, self._connects)
            group1.change_group(new_group)
            group2.change_group(new_group)

    def diagonal_join(self, guest):
        if self.position[1] - guest.position[1] < 0:  # SE_NW_DIAG
            join_type = GroupPosition.SE_NW_DIAGONAL
        else:
            join_type = GroupPosition.SW_NE_DIAGONAL

        diag_group = self.get_group(join_type)
        if diag_group is None:
            return None
        else:
            diag_group.update(guest)
            guest_diag_group = guest.get_group(join_type)
            if guest_diag_group is None:
                guest.set_group(diag_group, join_type)
            else:  # group merge required
                self._merge_groups(guest_diag_group, self.get_group(join_type))

            return diag_group

    def __str__(self):
        if self._player1:
            return "x"
        return "o"

    def create_vertical_group_with(self, guest):
        new_group = Group(guest, self, GroupPosition.VERTICAL, self._connects)
        self.set_group(new_group, GroupPosition.VERTICAL)
        guest.set_group(new_group, GroupPosition.VERTICAL)

    def create_horizontal_group_with(self, guest):
        hor_group = self.get_group(GroupPosition.HORIZONTAL)
        if hor_group is None:  # need to create one new group
            new_group = Group(self, guest, GroupPosition.HORIZONTAL, self._connects)
            self.set_group(new_group, GroupPosition.HORIZONTAL)
            guest.set_group(new_group, GroupPosition.HORIZONTAL)
        else:
            hor_group.update(guest)
            guest.set_group(hor_group, GroupPosition.HORIZONTAL)

    def create_diagonal_group_with(self, guest):
        if self.position[1] - guest.position[1] > 0:  # SE_NW_Diagonal
            group_position = GroupPosition.SE_NW_DIAGONAL
        else:  # SW_NE_DIAGONAL
            group_position = GroupPosition.SW_NE_DIAGONAL

        diag_group = self.get_group(group_position)
        if diag_group is None:
            new_group = Group(guest, self, group_position, self._connects)
            self.set_group(new_group, group_position)
            guest.set_group(new_group, group_position)
        else:
            diag_group.update(guest)
            guest.set_group(diag_group, group_position)
