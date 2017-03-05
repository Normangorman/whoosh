"""
This is where the InputSnapshot class lives.
"""
from whoosh.maths import Vec2f


class InputSnapshot:
    """
    A snapshot of a player's input at a point in time.
    This includes key presses, mouse presses and mouse aim position
    """
    def __init__(self):
        self.keys = {}
        self.mouse = {}
        self.screen_aim_pos = Vec2f() # position on the screen that the mouse is in
        self.world_aim_pos = Vec2f() # position in the world the mouse is in

    def is_key_pressed(self, key):
        return bool(self.keys.get(key))

    def is_mouse_pressed(self, button):
        return bool(self.mouse.get(button))

    def get_world_aim_pos(self):
        return self.world_aim_pos

    def get_screen_aim_pos(self):
        return self.screen_aim_pos

    def set_world_aim_pos(self, pos):
        self.world_aim_pos = pos

    def set_screen_aim_pos(self, pos):
        self.screen_aim_pos = pos

    def set_key_pressed(self, key):
        self.keys[key] = True

    def set_key_released(self, key):
        self.keys[key] = False

    def set_mouse_pressed(self, button):
        self.mouse[button] = True

    def set_mouse_released(self, button):
        self.mouse[button] = False

    def set_mouse_position(self, pos):
        self.mouse_pos = pos
