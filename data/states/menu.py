import pygame as pg

from .. import tools
from ..components.button import Button
from ..components.label import Label


class Menu(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def make_image(self):
        menu_image = pg.sprite.Sprite()
        image = pg.Surface((800, 600)).convert()
        image.fill(pg.Color('#4D6DE3'))
        inner_image = pg.Surface((700, 500)).convert()
        inner_image.fill(pg.Color('#C7EEFF'))
        image.blit(inner_image, (50, 50))
        label = Label(None, 45, 'FIFTEEN PUZZLE', pg.Color('black'),
                      center=(image.get_width() // 2, 115))
        image.blit(label.image, label.rect)
        menu_image.image = image
        menu_image.rect = image.get_rect(topleft=(0, 0))
        return menu_image

    def lock_image(self):
        self.buttons = self.make_buttons()
        self.buttons.draw(self.menu_image.image)

    def make_buttons(self):
        buttons = pg.sprite.Group()
        button_single = Button((400, 225), 'SINGLE PLAYER', None, 25,
                               self.button_call_single)
        button_two_players = Button((400, 350), 'TWO PLAYERS', None, 25,
                                    self.button_call_two_players)
        button_vs_comp = Button((400, 475), 'VS COMP', None, 25,
                                self.button_call_vs_comp)
        buttons.add(button_single, button_two_players, button_vs_comp)
        return buttons

    def turn_game_on(self, mode='SINGLE'):
        self.lock_image()
        self.next = 'GAME'
        self.persist['mode'] = mode
        self.persist['menu_image'] = self.menu_image
        self.done = True

    def button_call_single(self):
        self.turn_game_on('SINGLE')

    def button_call_two_players(self):
        self.turn_game_on('TWO_PLAYERS')

    def button_call_vs_comp(self):
        self.turn_game_on('VS_COMP')

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        self.menu_image = self.make_image()
        self.buttons = self.make_buttons()
        self.quit_label = Label(None, 20, 'ESC = Quit', pg.Color('black'),
                                topleft=(670, 530))
        self.quit_label_cover = pg.Surface(self.quit_label.rect.size).convert()
        self.quit_label_cover.fill(pg.Color('#C7EEFF'))
        self.quit_label_cover.set_alpha(255)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click()

    def draw(self, surface):
        # surface.fill(pg.Color('gray'))
        surface.blit(self.menu_image.image, self.menu_image.rect)
        self.buttons.draw(surface)
        self.quit_label.draw(surface)
        surface.blit(self.quit_label_cover, self.quit_label.rect.topleft)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
        self.quit_label_cover.set_alpha(
            max(0, self.quit_label_cover.get_alpha() - 3))
        self.draw(surface)
