import pymunk
import unittest
from whoosh.components.physics import PhysicsComponent
from whoosh.blob import Blob
from whoosh.maths import Vec2f
from whoosh.gameworld import GameWorld


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

    def test_touching_ground(self):
        bob = Blob("bob")
        phys = PhysicsComponent(mass=1, moment=10, body_type=pymunk.Body.DYNAMIC)
        phys.add_rect(10, 10)
        phys.set_position(Vec2f(0, 100))
        bob.add_component(phys)

        wall = Blob("wall")
        wall_phys = PhysicsComponent(body_type=pymunk.Body.STATIC)
        wall_phys.add_rect(100, 20)
        wall_phys.set_position(Vec2f(0, 0))
        wall.add_component(wall_phys)

        world = GameWorld()
        world.add_blob(bob)
        world.add_blob(wall)

        world.update(0.01)
        self.assertFalse(phys.is_touching_ground())

        for _ in range(50):
            world.update(0.03)
            if phys.is_touching_ground():
                # Passed
                return
        self.fail()