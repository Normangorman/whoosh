import unittest
import pyglet.window.key as key
import pymunk
from whoosh.blob import Blob
from whoosh.components.input import InputComponent
from whoosh.components.physics import PhysicsComponent
from whoosh.maths import Vec2f


class TestInputComponent(unittest.TestCase):

    def test_is_key_pressed(self):
        inp = InputComponent()

        self.assertFalse(inp.is_key_pressed(key.UP))
        inp.set_key_pressed(key.UP)
        self.assertTrue(inp.is_key_pressed(key.UP))
        inp.set_key_released(key.UP)
        self.assertFalse(inp.is_key_pressed(key.UP))

    def test_was_key_pressed(self):
        inp = InputComponent(update_from_local_player=False)

        self.assertFalse(inp.was_key_pressed(key.LEFT))
        inp.set_key_pressed(key.LEFT)
        inp.on_pre_tick()
        self.assertTrue(inp.was_key_pressed(key.LEFT))

    def test_is_key_just_pressed(self):
        inp = InputComponent(update_from_local_player=False)
        inp.set_key_pressed(key.DOWN)
        self.assertTrue(inp.is_key_just_pressed(key.DOWN))

        inp.on_pre_tick()
        inp.set_key_pressed(key.DOWN)
        self.assertFalse(inp.is_key_just_pressed(key.DOWN))

    def test_get_aim_direction(self):
        blob = Blob("Dave")
        inp = InputComponent(update_from_local_player=False)
        phys = PhysicsComponent(body_type=pymunk.Body.STATIC)
        phys.set_position(Vec2f(0, 0))
        inp.set_world_aim_pos(Vec2f(100, 100))
        blob.add_component(inp)
        blob.add_component(phys)

        want = Vec2f(0.70710678, 0.70710678)
        have = inp.get_aim_direction()
        self.assertAlmostEqual(want.x, have.x)
        self.assertAlmostEqual(want.y, have.y)

        phys.set_position(Vec2f(100, 0))
        want = Vec2f(0, 1)
        have = inp.get_aim_direction()
        self.assertEqual(want, have)

    def test_is_facing_right(self):
        blob = Blob("Dave")
        inp = InputComponent(update_from_local_player=False)
        phys = PhysicsComponent(body_type=pymunk.Body.STATIC)
        phys.set_position(Vec2f(0, 0))
        inp.set_world_aim_pos(Vec2f(100, 100))
        blob.add_component(inp)
        blob.add_component(phys)

        self.assertTrue(inp.is_facing_right())

        phys.set_position(Vec2f(105, 0))
        self.assertFalse(inp.is_facing_right())
