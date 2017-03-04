"""
An InputComponent is a wonderful thing.
It allows a blob to receive key presses and mouse movements.
"""
import copy
import logging
import pyglet.window
import whoosh.engine.api
from whoosh.components.base import BaseComponent
from whoosh.inputsnapshot import InputSnapshot
from whoosh.engine.modules.userinput import UserInputModule

logger = logging.getLogger(__name__)


class InputComponent(BaseComponent):
    """
    An InputComponent is not just for player input.
    An AI player might have one too for example as it provides a generic way to get input from a blob.
    """
    def __init__(self, update_from_local_player=True):
        """
        If from_local_machine is True then input will be updated by checking the local key presses on each tick.
        """
        BaseComponent.__init__(self)
        self.input_last_tick = InputSnapshot()
        self.input_this_tick = InputSnapshot()
        self.update_from_local_player = update_from_local_player

    def on_pre_tick(self):
        # Do this on pre tick because scripts are going to be checking input during their on_tick
        self.input_last_tick = copy.deepcopy(self.input_this_tick)
        if self.update_from_local_player:
            logger.debug("InputComponent updating from local player")
            input_module = whoosh.engine.api.get_engine_module(UserInputModule)
            self.input_this_tick = copy.deepcopy(input_module.get_snapshot())

    def is_key_pressed(self, key):
        """
        Returns True/False whether the given key is pressed.
        """
        return self.input_this_tick.is_key_pressed(key)

    def was_key_pressed(self, key):
        """
        Returns True/False whether the given key was pressed on the previous tick.
        """
        return self.input_last_tick.is_key_pressed(key)

    def is_key_just_pressed(self, key):
        """
        Returns True/False whether the given key was pressed on this tick but not the last one.
        """
        return self.is_key_pressed(key) and not self.was_key_pressed(key)

    def set_key_pressed(self, key):
        """
        Sets the state of the given key to be pressed.
        """
        self.input_this_tick.set_key_pressed(key)

    def set_key_released(self, key):
        """
        Sets the state of the given key to be not pressed.
        """
        self.input_this_tick.set_key_released(key)
