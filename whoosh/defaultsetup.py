"""
Sets up the engine using some default settings.
This provides a basic way to create a new game.
"""
from whoosh.engine.core import WhooshCore
from whoosh.engine.modules.loggingsetup import LoggingSetupModule
from whoosh.engine.modules.resourceloading import ResourceLoadingModule
from whoosh.engine.modules.userinput import UserInputModule
from whoosh.engine.modules.cameracontrol import CameraControlModule
from whoosh.graphics.window import WhooshWindow


def default_core(resource_directory="."):
    """
    Creates a new engine with a default renderer and an empty world.
    """
    core = WhooshCore()
    core.add_module(LoggingSetupModule())
    core.add_module(ResourceLoadingModule(resource_directory))
    core.add_module(UserInputModule())
    core.add_module(CameraControlModule())
    return core

def default_window(core, width=800, height=600):
    window = WhooshWindow(core, 60, width=width, height=height)
    window.enable_camera_debug = True
    window.enable_fps_display = True
    window.enable_physics_debug = True
    return window
