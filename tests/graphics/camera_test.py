import unittest
import random
from whoosh.graphics.camera import Camera
from whoosh.maths import Vec2f


class TestCamera(unittest.TestCase):

    def test_zoom(self):
        cam = Camera()

        # Test that zoom is limited to min/max
        cam.zoom(1.0)
        cam.zoom(1.0)
        self.assertEqual(cam.current_zoom, Camera.MIN_ZOOM)

        cam.zoom(-1.0)
        cam.zoom(-1.0)
        self.assertEqual(cam.current_zoom, Camera.MAX_ZOOM)

    def test_screen_to_world(self):
        cam = Camera()
        cam.set_zoom(1.0)

        click = Vec2f(10, 10)
        have = cam.convert_screen_to_world(click)
        want = Vec2f(10, 10)
        self.assertEqual(have, want)

        cam.set_zoom(0.5)
        click = Vec2f(10, 10)
        have = cam.convert_screen_to_world(click)
        want = Vec2f(165, 125)
        self.assertEqual(have, want)

    def test_world_to_screen(self):
        cam = Camera()
        cam.set_zoom(1.0)

        pos = Vec2f(10, 10)
        have = cam.convert_world_to_screen(pos)
        want = Vec2f(10, 10)
        self.assertEqual(have, want)

        cam.set_zoom(0.5)
        pos = Vec2f(10, 10)
        have = cam.convert_world_to_screen(pos)
        want = Vec2f((10 - cam.x)/cam.current_zoom, (10 - cam.y)/cam.current_zoom)
        self.assertEqual(have, want)

    def test_world_screen_conversion(self):
        """
        Generate some random vectors and ensure that world_to_screen(screen_to_world(v)) is correct
        """
        cam = Camera()
        ru = random.uniform
        cam.set_zoom(ru(Camera.MIN_ZOOM, Camera.MAX_ZOOM))
        cam.pan(Vec2f(ru(-100, 100), ru(-100, 100)))
        for _ in range(50):
            rx = ru(-1000, 1000)
            ry = ru(-1000, 1000)
            v = Vec2f(rx, ry)
            have = cam.convert_world_to_screen(cam.convert_screen_to_world(v))
            self.assertAlmostEqual(v.x, have.x)
            self.assertAlmostEqual(v.y, have.y)


