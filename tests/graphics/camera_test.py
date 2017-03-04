import unittest
from whoosh.graphics.camera import Camera


class TestCamera(unittest.TestCase):

    def test_zoom(self):
        cam = Camera()

        self.assertEqual(cam.fov, cam.defaultfov)
        cam.zoom(0.1)
        self.assertLess(cam.fov, cam.defaultfov)
        cam.zoom(-0.2)
        self.assertGreater(cam.fov, cam.defaultfov)

        # Test that zoom is limited to min/max
        cam.zoom(1.0)
        self.assertEqual(cam.fov, cam.minfov)

        cam.zoom(-1.0)
        self.assertEqual(cam.fov, cam.maxfov)