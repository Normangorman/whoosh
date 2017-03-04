import unittest
from whoosh.engine.core import WhooshCore
from whoosh.engine.modules.loggingsetup import LoggingSetupModule


class TestCore(unittest.TestCase):

    def test_add_module(self):
        core = WhooshCore()
        module = LoggingSetupModule()
        core.add_module(module)
        self.assertIs(module, core.get_module(LoggingSetupModule))
