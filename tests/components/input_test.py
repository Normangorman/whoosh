import unittest
import pyglet.window.key as key
from whoosh.components.input import InputComponent


class TestInputComponent(unittest.TestCase):

    def test_is_key_pressed(self):
        inp = InputComponent()

        self.assertFalse(inp.is_key_pressed(key.UP))
        inp.set_key_pressed(key.UP)
        self.assertTrue(inp.is_key_pressed(key.UP))
        inp.set_key_released(key.UP)
        self.assertFalse(inp.is_key_pressed(key.UP))

    def test_was_key_pressed(self):
        inp = InputComponent(update_from_local_player=False)

        self.assertFalse(inp.was_key_pressed(key.LEFT))
        inp.set_key_pressed(key.LEFT)
        inp.on_pre_tick()
        self.assertTrue(inp.was_key_pressed(key.LEFT))

    def test_is_key_just_pressed(self):
        inp = InputComponent(update_from_local_player=False)
        inp.set_key_pressed(key.DOWN)
        self.assertTrue(inp.is_key_just_pressed(key.DOWN))

        inp.on_pre_tick()
        inp.set_key_pressed(key.DOWN)
        self.assertFalse(inp.is_key_just_pressed(key.DOWN))
