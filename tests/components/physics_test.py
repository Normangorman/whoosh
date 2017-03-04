import pymunk
import unittest
from whoosh.components.physics import PhysicsComponent
from whoosh.blob import Blob
from whoosh.maths import Vec2f


class TestPhysicsComponent(unittest.TestCase):

    def test_set_position(self):
        bob = Blob("bob")
        phys = PhysicsComponent(mass=1, moment=10, body_type=pymunk.Body.DYNAMIC)
        phys.add_circle(radius=5)
        phys.body.position = (10, 10)
        bob.add_component(phys)
        self.assertEqual(phys.body.position, (10, 10))

        phys.set_position(Vec2f(5, 5))
        self.assertEqual(phys.body.position, (5, 5))
