from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass


class EventListener(ABC):
    @abstractmethod
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    @abstractmethod
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    @abstractmethod
    def on_mouse_release(self, x, y, button, modifiers):
        pass

    @abstractmethod
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    @abstractmethod
    def on_key_press(self, symbol, modifiers):
        pass

    @abstractmethod
    def on_resize(self, width, height):
        pass
