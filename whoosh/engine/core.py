"""
The engine's engine. The mighty core.
"""
import logging
import whoosh.engine.api
from whoosh.gameworld import GameWorld
from whoosh.engine.hooker import EngineHooker

logger = logging.getLogger(__name__)


class WhooshCore:
    """
    It's fast.
    It's fun.
    """
    def __init__(self):
        self.game_world = GameWorld()
        self.modules = {} # maps module class to module instance
        self.window = None
        whoosh.engine.api.set_engine(self)

    def add_module(self, module):
        """
        Adds a module to the engine
        """
        if not isinstance(module, EngineHooker):
            raise ValueError("Module should be an instance of EngineHooker: {0}".format(module))
        logger.debug("Module added: {0}".format(module))
        self.modules[type(module)] = module

    def get_module(self, module_type):
        """
        Gets and returns the added module of the given type if it exists.
        """
        return self.modules.get(module_type)

    def itermodules(self):
        """
        Returns an iterator over the engine's modules.
        """
        return self.modules.values()

    def set_window(self, window):
        """
        Sets the window that the game is being played in.
        This method will also call the on_set_window hook for engine modules.
        """
        self.window = window
        for module in self.itermodules():
            module.on_set_window(window)

    def get_game_world(self):
        return self.game_world

    def new_world(self):
        """
        A utility method which creates a new GameWorld and sets it as the current world, then returns it.
        """
        logger.debug("New world created")
        self.game_world = whoosh.engine.gameworld.GameWorld()
        return self.game_world

    def update(self, dt):
        """
        Updates the game world
        """
        self.game_world.update(dt)

    def on_render(self):
        """
        Called whenever the window renders the game
        """
        for module in self.itermodules():
            module.on_render()
