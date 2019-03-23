import pygame
import json
import sys
from game import Game
from windows import MenuWindow, MainGameWindow, WindowType
from youtube_api import get_pewds_subs_count

class PewdsClickerGame(Game):
    def __init__(self):
        try:
            json_config = open("config.json")
            config = json.load(json_config)
            screen_width = config['screen_width']
            screen_height = config['screen_height']
            json_config.close()
        except:
            screen_width = 1080
            screen_height = 720
        super().__init__('PewdsClicker', screen_width, screen_height, 30)
        self.background_image = pygame.image.load('images/background_1.png').convert()

        self.create_windows()
        self.set_window(self.available_windows[WindowType.MENU_WINDOW])


    def create_windows(self):
        menu_window = MenuWindow(self._screen_width, self._screen_height)
        main_game_window = MainGameWindow(self._screen_width, self._screen_height)
        # store_window = StoreWindow(self._screen_width, self._screen_height)
        self.available_windows[WindowType.MENU_WINDOW] = menu_window
        self.available_windows[WindowType.MAIN_GAME_WINDOW] = main_game_window
        # self.available_windows[WindowType.STORE_WINDOW] = store_window

    def start_game(self):
        pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
        super().start_game()
        self.available_windows[WindowType.MAIN_GAME_WINDOW].kill_thread()
        sys.exit()





def main():
    game = PewdsClickerGame()
    game.start_game()



if __name__ == '__main__':
    main()