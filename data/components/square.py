import pygame as pg
from .label import Label


class Square(pg.sprite.Sprite):
    def __init__(self, position, size, label):
        pg.sprite.Sprite.__init__(self)
        self.clickable = False
        self.label = label
        self.idle_image, self.hover_image = self.make_images(size)
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=position)

    def make_images(self, size):
        image = pg.Surface((size, size)).convert()
        image.fill(pg.Color('black'))
        idle_image = image.copy()
        hover_image = image.copy()

        idle_inside_image = pg.Surface((size - 2, size - 2)).convert()
        idle_inside_image.fill(pg.Color('lightblue'))
        label = Label(
            None, int(size / 2.75), str(self.label), pg.Color('black'),
            center=(size // 2 - 1, size // 2 - 1))
        label.draw(idle_inside_image)
        idle_image.blit(idle_inside_image, (1, 1))

        hover_inside_image = pg.Surface((size - 2, size - 2)).convert()
        hover_inside_image.fill(pg.Color('lightgreen'))
        label.draw(hover_inside_image)
        hover_image.blit(hover_inside_image, (1, 1))
        return idle_image, hover_image

    def update(self, mouse_pos, movable):
        """
        Check if square is movable and hovered.
        """
        hover = self.rect.collidepoint(mouse_pos)
        self.clickable = hover and movable
        if self.clickable:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
