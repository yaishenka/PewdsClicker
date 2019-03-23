import pygame


class GameObject:
    def __init__(self, pos, w, h):
        self._bounds = pygame.rect.Rect(pos[0], pos[1], w, h)
        self._bounds.center = pos

    def update(self):
        pass

    def draw(self, surface):
        pass

    def handle_event(self, event):
        pass


class MainHero(GameObject):
    def __init__(self, x, y):

        self.original_image = pygame.image.load("images/brofist.png")
        self._double_zoomed_image = pygame.transform.scale2x(self.original_image)

        self.center = (x, y)

        self._current_image = self.original_image
        self.__zoomed = False

        super(MainHero, self).__init__(self.center, self.original_image.get_width(),
                                       self.original_image.get_height())

    def draw(self, surface):
        surface.blit(self._current_image, self._bounds)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if (self.__zoomed):
                self.__zoomed = False
                self._bounds = pygame.rect.Rect(self.center[0], self.center[1],
                                                self.original_image.get_width(), self.original_image.get_height())
                self._bounds.center = self.center
                self._current_image = self.original_image
            else:
                self._bounds = pygame.rect.Rect(self.center[0], self.center[1],
                                                self._double_zoomed_image.get_width(),
                                                self._double_zoomed_image.get_height())
                self._bounds.center = self.center
                self._current_image = self._double_zoomed_image
                self.__zoomed = True


class TextObject(GameObject):
    def __init__(self, x, y, text_func, color):
        super(TextObject, self).__init__((x, y), 0, 0)
        self._pos = (x, y)
        self._text_func = text_func
        self._color = color
        self._font_object = pygame.font.SysFont('Arial', 50)  # TODO from config
        self._bounds = self.get_surface(text_func())

    def draw(self, surface):
        self._bounds = self.get_surface(self._text_func())
        center_pos = (self._pos[0] - self._bounds.get_width() / 2, self._pos[1] - self._bounds.get_height() / 2)
        surface.blit(self._bounds, center_pos)

    def get_surface(self, text):
        text_surface = self._font_object.render(text,
                                                False,
                                                self._color)
        return text_surface


class FlashingTextObject(TextObject):
    def __init__(self, x, y, text_func, color):
        super(FlashingTextObject, self).__init__(x, y, text_func, color)
        self.__visible = False

    def draw(self, surface):
        if (self.__visible):
            self.__visible = False
        else:
            super(FlashingTextObject, self).draw(surface)
            self.__visible = True
