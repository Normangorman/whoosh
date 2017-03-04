import pymunk
import unittest
from whoosh.gameworld import GameWorld
from whoosh.blob import Blob
from whoosh.components.physics import PhysicsComponent


class TestGameWorld(unittest.TestCase):

    def test_add_blob(self):
        """
        When adding a Blob to the game world, it's physics component should be added too if it exists
        """
        donny = Blob("Donald Trump")
        phys = PhysicsComponent(body_type=pymunk.Body.STATIC)
        donny.add_component(phys)

        world = GameWorld()

        self.assertEqual(donny.get_netid(), 0)
        self.assertEqual(len(world.physics_world.bodies), 0)

        world.add_blob(donny)

        self.assertEqual(donny.get_netid(), 1)
        self.assertEqual(len(world.physics_world.bodies), 1)

    def test_gravity(self):
        space = pymunk.Space()
        space.gravity = (0.0, -900.0)

        phys = PhysicsComponent(mass=10.0, moment=pymunk.moment_for_circle(10.0, 0, 25))
        phys.add_circle(25)
        body = phys.body
        shape = phys.shapes[0]

        space.add(body)
        self.assertEqual(body.position, (0, 0))

        space.step(0.02)
        space.step(0.02)

        self.assertNotEqual(body.position, (0, 0))

    def test_gravity_in_game(self):
        einstein = Blob("Einstein")

        phys = PhysicsComponent(mass=10.0, moment=pymunk.moment_for_circle(10.0, 0, 25))
        phys.add_circle(25)
        einstein.add_component(phys)

        world = GameWorld()
        world.add_blob(einstein)

        self.assertEqual(phys.body.position, (0, 0))

        world.update(0.02)
        world.update(0.02)

        self.assertNotEqual(phys.body.position, (0, 0))
