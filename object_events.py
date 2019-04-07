from enum import Enum
from window_events import ChangeWindowEvent as WindowChangeWindowEvent


class ObjectEvent:
    class ObjectEventType(Enum):
        CHANGE_WINDOW = 0

    def __init__(self, type, is_window_event, *args, **kwargs):
        self._type = type
        self.is_window_event = is_window_event
        self._args = args
        self._kwargs = kwargs


class ChangeWindowEvent(ObjectEvent):
    def __init__(self, window_to_change):
        assert (window_to_change is not None)
        super(ChangeWindowEvent, self).__init__(
            self.ObjectEventType.CHANGE_WINDOW, True,
            window_to_change=window_to_change)

    def get_window_event(self):
        return WindowChangeWindowEvent(self._kwargs['window_to_change'])
