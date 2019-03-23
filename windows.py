from objects import TextObject, MainHero, FlashingTextObject
from window_events import ChangeWindowEvent
from enum import Enum
import pygame

class WindowType(Enum):
    GAME_WINDOW = 0
    MENU_WINDOW = 1
    MAIN_GAME_WINDOW = 2
    STORE_WINDOW = 3

class GameWindow:
    def __init__(self, screen_width, screen_height):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._objects = []
        self._events = []

    def update_objects(self):
        for o in self._objects:
            o.update()

    def get_window_events(self):
        events_list = self._events[:]
        self._events.clear()
        return events_list

    def draw_objects(self, surface):
        for o in self._objects:
            o.draw(surface)

    def add_object(self, object):
        self._objects.append(object)

    def handle_event(self, event):
        for o in self._objects:
            o.handle_event(event)


class MenuWindow(GameWindow):
    def __init__(self, screen_width, screen_height):
        super(MenuWindow, self).__init__(screen_width, screen_height)
        self.init_objects()

    def init_objects(self):
        t_o = TextObject(self._screen_width / 2, self._screen_height / 2, lambda: F'MenuWindow', (0,255,0))
        self.add_object(t_o)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._events.append(ChangeWindowEvent(WindowType.MAIN_GAME_WINDOW))
        super(MenuWindow, self).handle_event(event)


class MainGameWindow(GameWindow):
    def __init__(self, screen_width, screen_height, init_scores, ):
        super(MainGameWindow, self).__init__(screen_width, screen_height)
        self.scores = init_scores
        self.init_objects()

    def init_objects(self):
        score_counter = TextObject(self._screen_width / 2, 50, lambda: F'Subscribers: {self.scores}', (0, 255, 0))
        main_hero = MainHero(self._screen_width / 2, self._screen_height / 2)
        sub_text = FlashingTextObject(self._screen_width / 2, self._screen_height - 50, lambda: F'Subscribe to Pewdiepie!', (255,0,0))
        self.add_object(score_counter)
        self.add_object(main_hero)
        self.add_object(sub_text)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.scores += 1
        super(MainGameWindow, self).handle_event(event)


class StoreWindow(GameWindow):
    pass