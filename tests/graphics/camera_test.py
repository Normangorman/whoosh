import unittest
from whoosh.graphics.camera import Camera


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