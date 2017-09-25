class AI:
    def __init__(self, grid):
        self._grid = [[elem for elem in row] for row in grid]
        self._height = len(self._grid)
        self._width = len(self._grid[0])
        self.path = self.solve_puzzle().upper()
        self.step = 0

    def get_next_move(self):
        move = self.path[self.step]
        self.step += 1
        return move

    def current_position(self, target_row, target_col):
        number = target_row * self._height + target_col
        for row_num, row in enumerate(self._grid):
            if number in row:
                return (row_num, row.index(number))

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, \
                    "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, \
                    "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, \
                    "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, \
                    "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (target_row, target_col):
            return False
        for row_num in range(target_row + 1, len(self._grid)):
            for col_num in range(len(self._grid[0])):
                if (self.current_position(row_num, col_num) !=
                        (row_num, col_num)):
                    return False
        for col_num in range(target_col + 1, len(self._grid[0])):
            if (self.current_position(target_row, col_num) !=
                    (target_row, col_num)):
                return False
        return True

    def position_tile(self, target_row, target_col, tile_row, tile_col):
        """
        Returns a path that puts tile on target tile and zero tile left to it.
        """
        path = ''
        if tile_col == target_col:
            path += 'u' * (target_row - tile_row)
            path += 'lddru' * (target_row - tile_row - 1)
            path += 'ld'
        elif tile_row == target_row:
            if tile_col < target_col:
                path += 'l' * (target_col - tile_col)
                path += 'urrdl' * (target_col - tile_col - 1)
            else:
                path += 'r' * (tile_col - target_col)
                path += 'ulldr' * (tile_col - target_col - 1)
                path += 'ulld'
        else:
            path += 'u' * (target_row - tile_row)
            if tile_col < target_col:
                path += 'l' * (target_col - tile_col)
                if tile_row == 0:
                    path += 'drrul' * (target_col - tile_col - 1)
                else:
                    path += 'urrdl' * (target_col - tile_col - 1)
                path += 'dru'
            else:
                path += 'r' * (tile_col - target_col)
                if tile_row == 0:
                    path += 'dllur' * (tile_col - target_col - 1)
                    path += 'dlu'
                else:
                    path += 'ulldr' * (tile_col - target_col - 1)
                    path += 'ullddru'
            path += 'lddru' * (target_row - tile_row - 1)
            path += 'ld'
        return path

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        tile_row, tile_col = self.current_position(target_row, target_col)
        path = self.position_tile(target_row, target_col, tile_row, tile_col)
        self.update_puzzle(path)
        return path

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        path = 'ur'
        tile_row, tile_col = self.current_position(target_row, 0)
        if (tile_row, tile_col) != (target_row - 1, 0):
            if (tile_row, tile_col) == (target_row - 1, 1):
                path += 'l'
            else:
                path += self.position_tile(
                    target_row - 1, 1, tile_row, tile_col)
            path += 'ruldrdlurdluurddlur'
        path += 'r' * (len(self._grid[0]) - 2)
        self.update_puzzle(path)
        return path

    #############################################################
    # Phase two methods

    def row_invariant(self, target_col):
        """
        Checks whether all tiles in rows lower than 1 and ...
        """
        for row_num in range(len(self._grid)):
            for col_num in range(len(self._grid[0])):
                if row_num > 1 or col_num > target_col:
                    if (self.current_position(row_num, col_num) !=
                            (row_num, col_num)):
                        return False
        return True

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (0, target_col):
            return False
        return (self.row_invariant(target_col) and
                self.current_position(1, target_col) == (1, target_col))

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (1, target_col):
            return False
        return self.row_invariant(target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        path = 'ld'
        tile_row, tile_col = self.current_position(0, target_col)
        if (tile_row, tile_col) != (0, target_col - 1):
            if (tile_row, tile_col) == (1, target_col - 1):
                path += self.position_tile(
                    1, target_col - 1, tile_row - 1, tile_col)
            else:
                path += self.position_tile(
                    1, target_col - 1, tile_row, tile_col)
            path += 'urdlurrdluldrruld'
        self.update_puzzle(path)
        return path

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        tile_row, tile_col = self.current_position(1, target_col)
        path = self.position_tile(1, target_col, tile_row, tile_col)
        path += 'ur'
        self.update_puzzle(path)
        return path

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        path = 'ul'
        self.update_puzzle(path)
        count = 0
        while count < 3:
            count += 1
            path += 'rdlu'
            self.update_puzzle('rdlu')
            if test_2x2(self):
                return path
        return path

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        path = ''
        zero_row, zero_col = self.current_position(0, 0)
        start_path = 'r' * (self._width - zero_col - 1)
        start_path += 'd' * (self._height - zero_row - 1)
        self.update_puzzle(start_path)
        for row_num in range(self._height - 1, 1, -1):
            for col_num in range(self._width - 1, 0, -1):
                path += self.solve_interior_tile(row_num, col_num)
            path += self.solve_col0_tile(row_num)
        for col_num in range(self._width - 1, 1, -1):
            path += self.solve_row1_tile(col_num)
            path += self.solve_row0_tile(col_num)
        path += self.solve_2x2()
        return start_path + path

    def update(self, dt):
        self.tasks.update(dt * 1000)


def test_2x2(game):
    for row_num in range(len(game._grid)):
        for col_num in range(len(game._grid[0])):
            if game.current_position(row_num, col_num) != (row_num, col_num):
                return False
    return True
