import pygame as pg


class Timer(pg.sprite.Sprite):
    def __init__(self, location, size, width, height):
        self.reset()
        self.font = pg.font.Font(None, size)
        self.empty_image = self.make_empty_image(width, height)
        self.update_image()
        self.rect = self.image.get_rect(topleft=location)

    def make_empty_image(self, width, height):
        image = pg.Surface((width, height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        return image

    def update_image(self):
        minutes = (self.minutes if len(str(self.minutes)) == 2
                   else '0' + str(self.minutes))
        seconds = (self.seconds if len(str(self.seconds)) == 2
                   else '0' + str(self.seconds))
        text = '{}:{}'.format(minutes, seconds)
        self.image = self.empty_image.copy()
        label = self.font.render(text, True, pg.Color('black'))
        rect = label.get_rect(center=(self.image.get_width() // 2,
                                      self.image.get_height() // 2))
        self.image.blit(label, rect)

    def reset(self):
        self.time = 0
        self.minutes = 0
        self.seconds = 0

    def update(self, dt):
        self.time += dt
        while self.time > 1:
            self.time -= 1
            self.seconds += 1
            if self.seconds >= 60:
                self.minutes += 1
                self.seconds -= 60
            self.update_image()
