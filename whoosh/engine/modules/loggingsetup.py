"""
In which the logging is set up.
ONLY TO BE TORN DOWN AGAIN.
Ok not really.
Logging is good.
"""
import logging
from whoosh.engine.hooker import EngineHooker


class LoggingSetupModule(EngineHooker):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
