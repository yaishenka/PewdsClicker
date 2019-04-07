from enum import Enum
import traceback


class WindowEvent:
    class WindowEventType(Enum):
        CHANGE_WINDOW = 0

    def __init__(self, type, *args, **kwargs):
        self._type = type
        self._args = args
        self._kwargs = kwargs

    def __call__(self, game_object):
        pass


class ChangeWindowEvent(WindowEvent):
    def __init__(self, window_to_change):
        assert (window_to_change is not None)
        super(ChangeWindowEvent, self).__init__(
            self.WindowEventType.CHANGE_WINDOW,
            window_to_change=window_to_change)

    def __call__(self, game_object):
        try:
            game_object.set_window(game_object.available_windows.get(
                self._kwargs['window_to_change']))
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
