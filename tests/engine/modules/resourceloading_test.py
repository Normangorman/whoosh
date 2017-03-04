import unittest
import pyglet
from whoosh.engine.modules.resourceloading import ResourceLoadingModule


class TestResourceLoading(unittest.TestCase):

    def test_it(self):
        module = ResourceLoadingModule("examples")
        loader = module.get_loader()
        image = loader.image("fireball_sprite.png")
