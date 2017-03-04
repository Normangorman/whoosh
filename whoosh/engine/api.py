"""
This represents the API that game scripts should use to interact with the engine.
"""
import logging

logger = logging.getLogger(__name__)
_ENGINE = None # A GLOBAL VARIABLE!? OFF WITH HIS HEAD

def set_engine(engine):
    logger.debug("API set_engine called")
    global _ENGINE
    if _ENGINE != None:
        raise Exception("Someone is trying to create a second engine! OFF WITH THEIR HEAD!")
    _ENGINE = engine

def get_engine_module(module_type):
    logger.debug("API get_engine_module({0}) called")
    _check_engine()
    global _ENGINE
    return _ENGINE.get_module(module_type)

def get_game_world():
    _check_engine()
    global _ENGINE
    return _ENGINE.get_game_world()

def _check_engine():
    global _ENGINE
    if not _ENGINE:
        raise Exception("ENGINE not set yet")
