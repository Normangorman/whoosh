import unittest
import pyglet.window.key
from whoosh.engine.modules.userinput import UserInputModule


class TestUserInput(unittest.TestCase):

    def test_is_key_pressed(self):
        module = UserInputModule()

        self.assertFalse(module.is_key_pressed(pyglet.window.key.UP))
        module.on_key_press(pyglet.window.key.UP, None)

        self.assertTrue(module.is_key_pressed(pyglet.window.key.UP))
        
