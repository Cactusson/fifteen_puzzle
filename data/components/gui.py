"""
The GUI of the game.
"""

import pygame as pg
from .square import Square
from .animations import Animation


class GUI:
    def __init__(self, location, square_size, gap_size, board):
        self.board = board
        self.move_distance = square_size + gap_size
        self.image = self.make_image(square_size, gap_size)
        self.rect = self.image.get_rect(topleft=location)
        self.squares = self.make_squares(square_size, gap_size)
        self.animations = pg.sprite.Group()

    def update_board(self, board):
        self.board = board

    def make_image(self, square_size, gap):
        image = pg.Surface(
            (square_size * 4 + gap * 5, square_size * 4 + gap * 5)).convert()
        image.fill(pg.Color('gray'))
        return image

    def make_squares(self, square_size, gap):
        squares = pg.sprite.Group()
        for row_num, row in enumerate(self.board):
            for col_num, label in enumerate(row):
                position = (self.rect.left + (square_size + gap) *
                            col_num + gap,
                            self.rect.top + (square_size + gap) *
                            row_num + gap)
                squares.add(Square(position, square_size, label))
        return squares

    def move_square(self, label, direction, callback):
        for square in self.squares:
            if square.label == label:
                if direction == 'U':
                    x = square.rect.left
                    y = square.rect.top + self.move_distance
                elif direction == 'D':
                    x = square.rect.left
                    y = square.rect.top - self.move_distance
                elif direction == 'L':
                    x = square.rect.left + self.move_distance
                    y = square.rect.top
                elif direction == 'R':
                    x = square.rect.left - self.move_distance
                    y = square.rect.top
                animation = Animation(x=x, y=y, duration=500,
                                      round_values=True)
                animation.callback = callback
                animation.start(square.rect)
                self.animations.add(animation)
                # square.move(direction, self.move_distance)

    def click_square(self):
        for square in self.squares:
            square.click()

    def update_squares(self, clickable):
        mouse_pos = pg.mouse.get_pos()
        for square in self.squares:
            square.update(mouse_pos, square.label in clickable)
        # self.update_image()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for square in self.squares:
            if square.label == 0:
                continue
            surface.blit(square.image, square.rect)
