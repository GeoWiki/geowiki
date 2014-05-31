from features_server import Rect
import unittest


class RestTest(unittest.TestCase):

    def test_overlap(self):
        self.assertTrue(Rect.overlap([0,0,2,2], [1,1,3,3]))
        self.assertFalse(Rect.overlap([0,0,2,2], [3,3,4,4]))

        with self.assertRaises(ValueError):
            Rect.overlap([0,0,2,2], [5,5,0,0])
