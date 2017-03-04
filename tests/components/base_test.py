import unittest
from whoosh.components.input import InputComponent
from whoosh.blob import Blob


class TestBaseComponent(unittest.TestCase):

    def test_get_blob(self):
        # It's not possible to actually make a BaseComponent so use InputComponent instead
        pam = Blob("Pamela Anderson")
        inp = InputComponent()
        self.assertIs(inp.get_blob(), None)
        pam.add_component(inp)
        self.assertIs(inp.get_blob(), pam)
