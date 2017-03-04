"""
This module gives game scripts an interface to the window's camera.
"""
import logging
import pyglet.window.mouse as mouse
import pyglet.window.key as key
from whoosh.components.physics import PhysicsComponent
from whoosh.engine.hooker import EngineHooker
from whoosh.graphics.camera import Camera
from whoosh.maths import Vec2f
from whoosh.blob import Blob

logger = logging.getLogger(__name__)


class CameraControlModule(EngineHooker):
    """
    Used to give scripts an interface to the camera.
    """
    PAN_AMOUNT = 10

    def __init__(self):
        self.window = None
        self.focus_blob = None

    def on_set_window(self, window):
        window.push_handlers(self)
        self.window = window

    def on_render(self):
        if self.focus_blob:
            # TODO: use blob transform?
            phys = self.focus_blob.get_component(PhysicsComponent)
            if phys:
                pos = phys.get_position()
                self.center_on(pos)

    def set_focus_blob(self, blob):
        """
        Sets a Blob to focus on. The camera will then automatically center on this blob as it moves.
        """
        if not isinstance(blob, Blob):
            raise ValueError("Invalid blob parameter {0}".format(blob))
        self.focus_blob = blob

    def pan(self, vec):
        self.window.get_camera().pan(vec)

    def zoom(self, amount):
        self.window.get_camera().zoom(amount)

    def rotate(self, vec):
        self.window.get_camera().rotate(vec)

    def set_zoom(self, zoom):
        self.window.get_camera().set_zoom(amount)

    def center_on(self, pos):
        self.window.get_camera().center_on(pos)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Window mouse press event handler
        """
        logger.debug("Mouse pressed: {0}".format(button))
        if button == mouse.MIDDLE: # set default zoom on middle mouse press
            self.set_zoom(0.5)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        Window mouse scroll event handler
        """
        self.zoom(scroll_y * 0.1)

    def on_key_press(self, symbol, modifiers):
        """
        Window key press event handler
        Pans the camera if the arrow keys are pressed
        """
        if self.focus_blob: # if we're focusing on a blob then don't allowing manual panning
            return
        pan = CameraControlModule.PAN_AMOUNT
        if symbol == key.LEFT:
            self.pan(Vec2f(-pan, 0))
        if symbol == key.RIGHT:
            self.pan(Vec2f(pan, 0))
        if symbol == key.UP:
            self.pan(Vec2f(0, -pan))
        if symbol == key.DOWN:
            self.pan(Vec2f(0, pan))