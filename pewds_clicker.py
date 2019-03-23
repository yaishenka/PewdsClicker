import pygame
import json
from game import Game
from windows import MenuWindow, MainGameWindow, StoreWindow, WindowType

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
        super(PewdsClickerGame, self).__init__('PewdsClicker', screen_width, screen_height, 90)
        self.background_image = pygame.image.load('images/background.png').convert()

        self.create_windows()
        self.set_window(self.available_windows[WindowType.MENU_WINDOW])


    def create_windows(self):
        menu_window = MenuWindow(self._screen_width, self._screen_height)
        main_game_window = MainGameWindow(self._screen_width, self._screen_height, 0)
        store_window = StoreWindow(self._screen_width, self._screen_height)
        self.available_windows[WindowType.MENU_WINDOW] = menu_window
        self.available_windows[WindowType.MAIN_GAME_WINDOW] = main_game_window
        self.available_windows[WindowType.STORE_WINDOW] = store_window




def main():
    game = PewdsClickerGame()
    game.start_game()



if __name__ == '__main__':
    main()