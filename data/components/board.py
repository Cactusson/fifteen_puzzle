import pygame as pg
import random

from .ai import AI
from .fifteen_puzzle import FifteenPuzzle
from .gui import GUI
from .task import Task


class Board:
    def __init__(self, position, square_size, gap_size,
                 keys=None, mouse=False, ai=False):
        self.finished = False
        self.keys = keys
        self.mouse = mouse
        grid = [[1, 0, 2, 3], [4, 5, 6, 7],
                [8, 9, 10, 11], [12, 13, 14, 15]]
        self.fifteen_puzzle = FifteenPuzzle(init_board=grid)
        self.fifteen_puzzle.shuffle_board()
        if self.mouse:
            self.clickable_squares = self.fifteen_puzzle.get_movable_squares()
        self.gui = GUI(position, square_size, gap_size,
                       self.fifteen_puzzle.board)
        self.tasks = pg.sprite.Group()
        if ai:
            self.ai = AI(self.fifteen_puzzle.board)
            self.ai_wait()
        else:
            self.ai = None

    def make_move(self, direction):
        if (not self.fifteen_puzzle.is_move_possible(direction) or
                self.gui.animations):
            return
        target_row, target_col = self.fifteen_puzzle.get_target(direction)
        label = self.fifteen_puzzle.board[target_row][target_col]
        self.current_move = direction
        self.gui.move_square(label, direction, self.animation_ends)
        self.clickable_squares = []
        self.move_counter.increase_count()

    def mouse_click(self):
        for square in self.gui.squares:
            if square.clickable:
                self.make_move(self.fifteen_puzzle.get_direction(square.label))

    def animation_ends(self):
        self.fifteen_puzzle.apply_move(self.current_move)
        if self.mouse:
            self.clickable_squares = self.fifteen_puzzle.get_movable_squares()
        if self.ai:
            self.ai_wait()

    def check_finished(self):
        self.finished = self.fifteen_puzzle.is_finished()
        return self.finished

    def ai_make_move(self):
        move = self.ai.get_next_move()
        self.make_move(move)

    def ai_wait(self):
        time = random.randint(500, 1500)
        self.tasks.add(Task(self.ai_make_move, time))

    def draw(self, surface):
        self.gui.draw(surface)

    def update(self, dt):
        self.gui.animations.update(dt * 1000)
        if self.mouse:
            self.gui.update_squares(self.clickable_squares)
        if self.ai:
            self.tasks.update(dt * 1000)
