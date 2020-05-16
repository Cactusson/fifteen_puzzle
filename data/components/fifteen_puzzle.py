"""
The logic of the game.
"""

import random


class FifteenPuzzle:
    def __init__(self, init_board=None):
        self.height = self.width = 4
        if init_board:
            self.board = [[elem for elem in row] for row in init_board]
        else:
            self.board = [[0, 1, 2, 3], [4, 5, 6, 7],
                          [8, 9, 10, 11], [12, 13, 14, 15]]

    def shuffle_board(self):
        numbers = [elem for row in self.board for elem in row]
        random.shuffle(numbers)
        for row_num in range(self.height):
            self.board[row_num] = numbers[
                row_num*self.width:row_num*self.width+4]
        if self.is_finished():
            self.shuffle_board()

    def is_finished(self):
        return self.board == [[0, 1, 2, 3], [4, 5, 6, 7],
                              [8, 9, 10, 11], [12, 13, 14, 15]]

    def current_position(self, target_row, target_col):
        number = target_row * self.height + target_col
        for row_num, row in enumerate(self.board):
            if number in row:
                return (row_num, row.index(number))

    def is_move_possible(self, move):
        if move == 'U':
            return 0 not in self.board[0]
        elif move == 'D':
            return 0 not in self.board[-1]
        elif move == 'L':
            return 0 not in [row[0] for row in self.board]
        elif move == 'R':
            return 0 not in [row[-1] for row in self.board]

    def get_target(self, move):
        row_num, col_num = self.current_position(0, 0)
        if move == 'U':
            target_row, target_col = row_num - 1, col_num
        elif move == 'D':
            target_row, target_col = row_num + 1, col_num
        elif move == 'L':
            target_row, target_col = row_num, col_num - 1
        elif move == 'R':
            target_row, target_col = row_num, col_num + 1
        return target_row, target_col

    def apply_move(self, move):
        target_row, target_col = self.get_target(move)
        row_num, col_num = self.current_position(0, 0)
        (self.board[row_num][col_num], self.board[target_row][target_col]) = \
            (self.board[target_row][target_col], self.board[row_num][col_num])

    def get_direction(self, label):
        label_row = label_col = None
        for row_num, row in enumerate(self.board):
            for col_num, elem in enumerate(row):
                if self.board[row_num][col_num] == label:
                    label_row, label_col = row_num, col_num
                    break
            if label_row is not None:
                break
        zero_row, zero_col = self.current_position(0, 0)
        if label_row < zero_row:
            return 'U'
        elif label_row > zero_row:
            return 'D'
        elif label_col < zero_col:
            return 'L'
        elif label_col > zero_col:
            return 'R'

    def get_movable_squares(self):
        zero_row, zero_col = self.current_position(0, 0)
        result = []
        if zero_row >= 1:
            result.append(self.board[zero_row - 1][zero_col])
        if zero_row + 1 < self.height:
            result.append(self.board[zero_row + 1][zero_col])
        if zero_col >= 1:
            result.append(self.board[zero_row][zero_col - 1])
        if zero_col + 1 < self.width:
            result.append(self.board[zero_row][zero_col + 1])
        return result
