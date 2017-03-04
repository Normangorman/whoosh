"""
In which the logging is set up.
ONLY TO BE TORN DOWN AGAIN.
Ok not really.
Logging is good.
"""
import logging
from whoosh.engine.hooker import EngineHooker


class LoggingSetupModule(EngineHooker):

    def on_init(self):
        logging.basicConfig(level=logging.INFO)
