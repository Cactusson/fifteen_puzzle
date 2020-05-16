import pygame as pg
import random

from .. import prepare, tools
from ..components.animations import Animation
from ..components.board import Board
from ..components.label import Label
from ..components.move_counter import MoveCounter
from ..components.timer import Timer


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.animations = pg.sprite.Group()
        self.ornaments = pg.sprite.Group()
        self.quit_label = Label(None, 20, 'ESC = Quit', pg.Color('black'),
                                topleft=(720, 580))
        # self.state could be PLAY, PRE_PLAY, WIN

    def start(self):
        """
        Starts the game. Used in the beginning and then at every restart.
        """
        self.ornaments.empty()
        self.state = 'PRE_PLAY'
        self.timer = Timer((350, 0), 30, 100, 50)
        if self.mode == 'SINGLE':
            single_board = Board(
                (200, 100), 100, 2,
                keys={pg.K_UP: 'U', pg.K_DOWN: 'D',
                      pg.K_LEFT: 'L', pg.K_RIGHT: 'R'},
                mouse=True)
            move_counter = MoveCounter((200, 75), 30, 100, 25)
            single_board.move_counter = move_counter
            self.boards = [single_board]
        elif self.mode == 'TWO_PLAYERS':
            first_board = Board(
                (50, 150), 75, 1,
                keys={pg.K_w: 'U', pg.K_s: 'D',
                      pg.K_a: 'L', pg.K_d: 'R'},
                mouse=False)
            move_counter = MoveCounter((50, 125), 25, 100, 25)
            first_board.move_counter = move_counter
            second_board = Board(
                (450, 150), 75, 1,
                keys={pg.K_UP: 'U', pg.K_DOWN: 'D',
                      pg.K_LEFT: 'L', pg.K_RIGHT: 'R'},
                mouse=False)
            move_counter = MoveCounter((450, 125), 25, 100, 25)
            second_board.move_counter = move_counter
            self.boards = [first_board, second_board]
        elif self.mode == 'VS_COMP':
            player_board = Board(
                (50, 150), 75, 1,
                keys={pg.K_UP: 'U', pg.K_DOWN: 'D',
                      pg.K_LEFT: 'L', pg.K_RIGHT: 'R'},
                mouse=True)
            move_counter = MoveCounter((50, 125), 25, 100, 25)
            player_board.move_counter = move_counter
            comp_board = Board(
                (450, 150), 75, 1,
                keys=None,
                mouse=False,
                ai=True)
            move_counter = MoveCounter((450, 125), 25, 100, 25)
            comp_board.move_counter = move_counter
            self.boards = [player_board, comp_board]

    def move_menu_image(self):
        side = random.randint(1, 4)
        if side == 1:
            x = -self.menu_image.rect.width
            y = 0
        elif side == 2:
            x = 801
            y = 0
        elif side == 3:
            x = 0
            y = -self.menu_image.rect.height
        elif side == 4:
            x = 0
            y = 601
        animation = Animation(x=x, y=y, duration=750, transition='in_quad',
                              round_values=True)
        animation.start(self.menu_image.rect)
        animation.callback = self.start_play
        self.animations.add(animation)

    def start_play(self):
        self.state = 'PLAY'

    def win(self):
        self.state = 'WIN'
        for board in self.boards:
            if board.check_finished():
                ornament = self.create_ornament(board, True)
            else:
                ornament = self.create_ornament(board, False)
            x = board.gui.rect.x
            y = ornament.rect.top - board.move_counter.rect.height
            animation = Animation(x=x, y=y, duration=500,
                                  transition='out_quad', round_values=True)
            animation.start(board.move_counter.rect)
            self.animations.add(animation)

    def create_ornament(self, board, won=True):
        if won:
            text = 'WON'
            color = pg.Color('#7BC74D')
        else:
            text = 'LOST'
            color = pg.Color('#D72323')
        ornament = pg.sprite.Sprite()
        image = pg.Surface(
            (1.1 * board.gui.rect.width,
             1.5 * board.gui.rect.height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        inner_image = pg.Surface(
            (1.1 * board.gui.rect.width,
             1.1 * board.gui.rect.height)).convert()
        inner_image.fill(color)
        label = Label(None, 35, text, color, center=(
            image.get_width() // 2, inner_image.get_height() * 1.1))
        image.blit(inner_image, (0, 0))
        image.blit(label.image, label.rect)
        ornament.image = image
        ornament.rect = ornament.image.get_rect(
            topleft=(board.gui.rect.left - 0.05 * board.gui.rect.width,
                     board.gui.rect.top - 0.05 * board.gui.rect.height))
        self.ornaments.add(ornament)
        return ornament

    def escape(self):
        side = random.randint(1, 4)
        if side == 1:
            self.menu_image.rect.x = -self.menu_image.rect.width
            self.menu_image.rect.y = 0
        elif side == 2:
            self.menu_image.rect.x = 801
            self.menu_image.rect.y = 0
        elif side == 3:
            self.menu_image.rect.x = 0
            self.menu_image.rect.y = -self.menu_image.rect.height
        elif side == 4:
            self.menu_image.rect.x = 0
            self.menu_image.rect.y = 601
        self.state = 'PRE_PLAY'
        animation = Animation(x=0, y=0, duration=750, transition='out_quad',
                              round_values=True)
        animation.start(self.menu_image.rect)
        animation.callback = self.turn_to_menu
        self.animations.add(animation)

    def turn_to_menu(self):
        self.next = 'MENU'
        self.done = True

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        if 'mode' in self.persist:
            self.mode = self.persist['mode']
        else:
            self.mode = 'VS_COMP'  # 'SINGLE', 'TWO_PLAYERS', 'VS_COMP'
        self.menu_image = self.persist['menu_image']
        self.start()
        self.move_menu_image()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.state != 'PRE_PLAY':
                    self.escape()
            elif event.key == pg.K_SPACE:
                self.start()
            elif self.state == 'PLAY':
                for board in self.boards:
                    if board.keys and event.key in board.keys:
                        board.make_move(board.keys[event.key])
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.state == 'PLAY':
                for board in self.boards:
                    if board.gui.rect.collidepoint(event.pos) and board.mouse:
                        board.mouse_click()

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        for ornament in self.ornaments:
            surface.blit(ornament.image, ornament.rect)
        for board in self.boards:
            board.draw(surface)
            board.move_counter.draw(surface)
        surface.blit(self.timer.image, self.timer.rect)
        self.quit_label.draw(surface)
        surface.blit(self.menu_image.image, self.menu_image.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        if self.state == 'PLAY':
            self.timer.update(dt)
            for board in self.boards:
                board.update(dt)
                if board.check_finished():
                    self.win()
        self.animations.update(dt * 1000)
        self.draw(surface)
