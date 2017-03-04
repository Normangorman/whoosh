"""
In which stuff is loaded into the game.
"""
import pyglet
import os
from whoosh.engine.hooker import EngineHooker


class ResourceLoadingModule(EngineHooker):
    """
    A nice layer on top of pyglet's resource loading
    """
    def __init__(self, resource_directory="."):
        self.loader = None
        self.set_resource_directory(resource_directory)

    def get_loader(self):
        """
        Get a loader this
        """
        return self.loader

    def set_resource_directory(self, directory):
        """
        Sets the directory in which resources will be looked for.
        """
        if not os.path.isdir(directory):
            raise ValueError("That's not a directory! {0}".format(directory))
        self.loader = pyglet.resource.Loader(script_home=directory)
