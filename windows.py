from objects import TextObject, MainHero, FlashingTextObject
from window_events import ChangeWindowEvent
from bonuses import Bonus, BotNetBonus, AdvertisingBonus
from enum import Enum
from threading import Thread
import time
from youtube_api import get_tseries_subs_count, get_pewds_subs_count
import pygame
import json


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
        super().__init__(screen_width, screen_height)
        self.init_objects()

    def init_objects(self):
        press_space = TextObject(self._screen_width / 2,
                                 self._screen_height / 2,
                                 lambda: F'Press Space to play!',
                                 (0, 255, 0))
        github_url = TextObject(self._screen_width / 2,
                                self._screen_height - 30,
                                lambda: F'github.com/yaishenka',
                                (255, 0, 0), 30)
        self.add_object(press_space)
        self.add_object(github_url)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._events.append(ChangeWindowEvent(WindowType.MAIN_GAME_WINDOW))
        super().handle_event(event)


class MainGameWindow(GameWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)

        self.bonuses = {}
        self.__updater_thread = Thread(target=self.update_tseries_subs)
        self.__stop_thread = False

        with open('youtube_api_key.json') as json_api_key:
            self.__api_key = json.load(json_api_key)['api_key']

        self.init_counters()
        self.init_objects()
        self.init_store()
        self.__updater_thread.start()

    def init_store(self):
        self.bonuses[Bonus.BonusType.SUBS] = BotNetBonus()
        self.bonuses[Bonus.BonusType.MONEY_PER_FRAME] = AdvertisingBonus()
        botnet_bonus_text = TextObject(1.5 * self._screen_width / 8, 250,
                                       self.bonuses[
                                           Bonus.BonusType.SUBS].get_presentation,
                                       (0, 0, 0), 20)
        advert_bonus_text = TextObject(1.5 * self._screen_width / 8, 280,
                                       self.bonuses[
                                           Bonus.BonusType.MONEY_PER_FRAME].get_presentation,
                                       (0, 0, 0), 20)
        self.add_object(botnet_bonus_text)
        self.add_object(advert_bonus_text)

    def init_counters(self):
        self.scores = get_pewds_subs_count(self.__api_key)
        self.money = 0
        self.money_per_sec_ratio = 0.01 if not self.scores else 0.0000000001
        self.tseries_subs = get_tseries_subs_count(self.__api_key)

        score_counter = TextObject(self._screen_width / 2, 50,
                                   lambda: F'Subs: {self.scores}', (0, 255, 0))
        money_counter = TextObject(1.5 * self._screen_width / 8, 200,
                                   lambda: F'Money: {format(self.money, ".2f")}',
                                   (255, 0, 0), 30)
        if self.tseries_subs != 0:
            tseries_score_counter = TextObject(self._screen_width / 2, 100,
                                               lambda: F'TSeries subs: {self.tseries_subs}',
                                               (255, 0, 0), 30)
            self.add_object(tseries_score_counter)

        self.add_object(score_counter)
        self.add_object(money_counter)

    def init_objects(self):
        main_hero = MainHero(self._screen_width / 2, self._screen_height / 2)
        sub_text = FlashingTextObject(self._screen_width / 2,
                                      self._screen_height - 50,
                                      lambda: F'Subscribe to Pewdiepie!',
                                      (255, 0, 0))
        pause_text = TextObject(1.5 * self._screen_width / 8, 30,
                                lambda: F'P to pause', (255, 0, 0), 30)
        help_text = TextObject(1.5 * self._screen_width / 8, 310,
                               lambda: F'Press 1/2 to upgrade BotNet/Advert',
                               (255, 0, 0), 30)
        self.add_object(main_hero)
        self.add_object(sub_text)
        self.add_object(pause_text)
        self.add_object(help_text)

    def update_objects(self):
        self.money += self.money_per_sec()
        self.scores += self.subs_per_sec()
        super().update_objects()

    def kill_thread(self):
        self.__stop_thread = True
        self.__updater_thread.join()

    def money_per_sec(self):
        return (self.money_per_sec_ratio + self.bonuses[
            Bonus.BonusType.MONEY_PER_FRAME].get_bonus()) * self.scores

    def subs_per_sec(self):
        return self.bonuses[Bonus.BonusType.SUBS].get_bonus()

    def update_tseries_subs(self):
        while (not self.__stop_thread):
            real_subs = get_tseries_subs_count(self.__api_key)
            if real_subs:
                self.tseries_subs = real_subs
            time.sleep(2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.scores += 1
            if event.key == pygame.K_p:
                self._events.append(ChangeWindowEvent(WindowType.MENU_WINDOW))
            if event.key == pygame.K_1:
                if self.money > self.bonuses[Bonus.BonusType.SUBS].get_price():
                    self.money -= self.bonuses[
                        Bonus.BonusType.SUBS].get_price()
                    self.bonuses[Bonus.BonusType.SUBS].level += 1
            if event.key == pygame.K_2:
                if self.money > self.bonuses[
                    Bonus.BonusType.MONEY_PER_FRAME].get_price():
                    self.money -= self.bonuses[
                        Bonus.BonusType.MONEY_PER_FRAME].get_price()
                    self.bonuses[Bonus.BonusType.MONEY_PER_FRAME].level += 1

        super().handle_event(event)
