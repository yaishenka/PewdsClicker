import pygame
import os
import json


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
        self.first_frame_image = pygame.image.load(
            os.path.join('images', 'hero_a.png'))
        self.second_frame_image = pygame.image.load(
            os.path.join('images', 'hero_b.png'))

        self.center = (x, y)

        self._current_image = self.first_frame_image
        self.__frame_changed = False

        super().__init__(self.center, self._current_image.get_width(),
                         self._current_image.get_height())

    def draw(self, surface):
        surface.blit(self._current_image, self._bounds)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if (self.__frame_changed):
                self.__frame_changed = False
                self._bounds = pygame.rect.Rect(self.center[0], self.center[1],
                                                self.first_frame_image.get_width(),
                                                self.first_frame_image.get_height())
                self._bounds.center = self.center
                self._current_image = self.first_frame_image
            else:
                self._bounds = pygame.rect.Rect(self.center[0], self.center[1],
                                                self.second_frame_image.get_width(),
                                                self.second_frame_image.get_height())
                self._bounds.center = self.center
                self._current_image = self.second_frame_image
                self.__frame_changed = True


class TextObject(GameObject):
    def __init__(self, x, y, text_func, color, font_size=50):
        super().__init__((x, y), 0, 0)
        self._pos = (x, y)
        self._text_func = text_func
        self._color = color
        try:
            with json.load(open('config.json')) as config:
                font_name = config['font_name']
        except:
            font_name = 'Arial'
        self._font_object = pygame.font.SysFont(font_name,
                                                font_size)
        self._bounds = self.get_surface(text_func())

    def draw(self, surface):
        self._bounds = self.get_surface(self._text_func())
        center_pos = (self._pos[0] - self._bounds.get_width() / 2,
                      self._pos[1] - self._bounds.get_height() / 2)
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
            super().draw(surface)
            self.__visible = True
