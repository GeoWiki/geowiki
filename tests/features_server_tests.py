import features_server
import unittest


class FeatureServerTest(unittest.TestCase):

    def test_get_features_in_bbox(self):
        server = features_server.FeaturesServer()
        bbox = [35, 18.48, 149, 7.47]
        features = server.get_features_in_bbox(bbox)
        self.assertEqual('Australia', features['name'])
