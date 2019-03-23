import pygame


class Game:
    def __init__(self, caption, screen_width, screen_height, frame_rate):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._frame_rate = frame_rate
        self._caption = caption

        self.available_windows = {}
        self.background_image = None
        self._current_window = None
        self.__game_over = False

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self._caption)
        self.__surface = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._clock = pygame.time.Clock()

    def set_window(self, window):
        if window is not None:
            self._current_window = window
        else:
            raise Exception("Window doesn't exists")

    def update(self):
        if self._current_window is not None:
            self._current_window.update_objects()

    def draw(self):
        if self._current_window is not None:
            self._current_window.draw_objects(self.__surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over = True
            if self._current_window is not None:
                self._current_window.handle_event(event)

    def handle_window_events(self):
        if self._current_window is not None:
            for window_event in self._current_window.get_window_events():
                window_event(self)

    def start_game(self):
        while not self.__game_over:
            if self.background_image is not None:
                self.__surface.blit(self.background_image, [0, 0])
            else:
                self.__surface.fill((0, 0, 255))
            self.handle_events()
            self.update()
            self.handle_window_events()
            self.draw()
            pygame.display.update()
            self._clock.tick(self._frame_rate)
        pygame.quit()
