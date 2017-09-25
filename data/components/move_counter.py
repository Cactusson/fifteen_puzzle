import pygame as pg


class MoveCounter(pg.sprite.Sprite):
    def __init__(self, location, font_size, width, height):
        self.count = 0
        self.font = pg.font.Font(None, font_size)
        self.empty_image = self.make_empty_image(width, height)
        self.update_image()
        self.rect = self.image.get_rect(topleft=location)

    def make_empty_image(self, width, height):
        image = pg.Surface((width, height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        return image

    def increase_count(self):
        self.count += 1
        self.update_image()

    def update_image(self):
        self.image = self.empty_image.copy()
        text = 'Moves: {}'.format(self.count)
        label = self.font.render(text, True, pg.Color('black'))
        rect = label.get_rect(center=(self.image.get_width() // 2,
                                      self.image.get_height() // 2))
        self.image.blit(label, rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
