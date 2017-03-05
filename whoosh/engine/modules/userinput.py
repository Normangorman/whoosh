"""
This module gives game scripts an interface to the user's mouse and keyboard.
"""
import logging
import whoosh.engine.api
from whoosh.engine.hooker import EngineHooker
from whoosh.inputsnapshot import InputSnapshot
from whoosh.maths import Vec2f

logger = logging.getLogger(__name__)


class UserInputModule(EngineHooker):
    """
    Used for managing mouse and keyboard input from the local user.
    Scripts can query the input with is_key_pressed.
    This class also acts an event handler and will be attached to the game's Window.
    """
    def __init__(self):
        self.snapshot = InputSnapshot()

    def get_snapshot(self):
        return self.snapshot

    def on_set_window(self, window):
        window.push_handlers(self)

    def is_key_pressed(self, key):
        return self.snapshot.is_key_pressed(key)

    def is_mouse_pressed(self, button):
        return self.snapshot.is_mouse_pressed(button)

    def get_world_aim_pos(self):
        return self.snapshot.get_world_aim_pos()

    def get_screen_aim_pos(self):
        return self.snapshot.get_world_aim_pos()

    def on_key_press(self, symbol, modifiers):
        """
        Window event handler
        """
        logger.debug("Key pressed: {0}".format(symbol))
        self.snapshot.set_key_pressed(symbol)

    def on_key_release(self, symbol, modifiers):
        """
        Window event handler
        """
        logger.debug("Key released: {0}".format(symbol))
        self.snapshot.set_key_released(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Window event handler
        """
        logger.debug("Mouse pressed: {0}".format(button))
        self.snapshot.set_mouse_pressed(button)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Window event handler
        """
        logger.debug("Mouse released: {0}".format(button))
        self.snapshot.set_mouse_released(button)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Window event handler
        """
        logger.debug("Mouse moved: ({0}, {1})".format(x, y))
        screen_aim = Vec2f(x, y)
        self.snapshot.set_screen_aim_pos(screen_aim)
        cam = whoosh.engine.api.get_camera()
        if cam == None:
            raise Exception("Couldn't get Camera")
        else:
            world_aim = cam.convert_screen_to_world(screen_aim)
            self.snapshot.set_world_aim_pos(world_aim)


