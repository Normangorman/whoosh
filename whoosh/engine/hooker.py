# -*- coding: utf-8 -*-
"""
( ͡° ͜ʖ ͡°)
"""
from abc import ABCMeta


class EngineHooker:
    """
    Inherit from this class if you want to hear about events in the engine.
    """
    __metaclass__ = ABCMeta

    def on_set_window(self, window):
        """
        Called when the window is set on the engine
        """
        pass

    def on_pre_tick(self):
        """
        Called just before every game tick
        """
        pass

    def on_tick(self):
        """
        Called every game tick
        """
        pass

    def on_post_tick(self):
        """
        Called just after every game tick
        """
        pass

    def on_render(self):
        """
        Called every time the window renders the game
        """
        pass
