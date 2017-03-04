import unittest
import whoosh.maths as maths


class TestMaths(unittest.TestCase):

    def test_degrees_to_radians(self):
        dtr = maths.degrees_to_radians
        rtd = maths.radians_to_degrees
        self.assertAlmostEqual(rtd(dtr(50.0)), 50.0)
        self.assertAlmostEqual(rtd(dtr(43.0)), 43.0)
        self.assertAlmostEqual(dtr(rtd(1.17)), 1.17)

    def test_get_ngon_vertices(self):
        diamond_verts = maths.get_ngon_vertices(1.0, 4)
        self.assertEqual(len(diamond_verts), 4)
        self.assertAlmostEqual(diamond_verts[0][0], 0.0)
        self.assertAlmostEqual(diamond_verts[0][1], -1.0)
        self.assertAlmostEqual(diamond_verts[1][0], 1.0)
        self.assertAlmostEqual(diamond_verts[1][1], 0.0)
        self.assertAlmostEqual(diamond_verts[2][0], 0.0)
        self.assertAlmostEqual(diamond_verts[2][1], 1.0)
        self.assertAlmostEqual(diamond_verts[3][0], -1.0)
        self.assertAlmostEqual(diamond_verts[3][1], 0.0)
