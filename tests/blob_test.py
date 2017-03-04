import unittest
from whoosh.blob import Blob
from whoosh.components.input import InputComponent


class TestBlob(unittest.TestCase):

    def test_tags(self):
        b = Blob("Charlie Parker")
        b.tag("cool")
        self.assertTrue(b.has_tag("cool"))

    def test_get_component(self):
        b = Blob("Dave Brubeck")
        inp = InputComponent()
        b.add_component(inp)
        self.assertIs(inp, b.get_component(InputComponent))

    def test_change_component(self):
        b = Blob("Ray Charles")
        inp = InputComponent()
        b.add_component(inp)
        def set_foo(x):
            x.foo = "bar"
        b.change_component(InputComponent, set_foo)
        self.assertEqual(inp.foo, "bar")
