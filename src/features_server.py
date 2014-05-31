import math
import shapefile
import feature


class TileUtils:
    """
    Свалка функций тайловой арифметики
    http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y
    """
    @staticmethod
    def tile_to_latlon(x, y, zoom):
        n = 2 ** zoom
        lon_deg = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return lat_deg, lon_deg,

    @staticmethod
    def get_tile_bbox(x, y, zoom):
        p1 = TileUtils.tile_to_latlon(x, y, zoom)
        p2 = TileUtils.tile_to_latlon(x + 1, y + 1, zoom)
        return p1[1], p2[0], p2[1], p1[0],

    @staticmethod
    def degrees_in_pixel(zoom):
        """
        Примерный размер 1 пиксела в градусах широты
        """
        return 90/(256*(2**zoom))


class Rect:
    """
    Свалка функций для работы с прямоугольниками.
    TODO: учесть случай, когда страна переваливает через 0, типа России
    """
    @staticmethod
    def range_overlap(a_min, a_max, b_min, b_max):
        """
        Ни один диапазон не строго больше или правее другого
        """
        return not ((a_min > b_max) or (b_min > a_max))

    @staticmethod
    def validate_range(min, max):
        if min > max:
            raise ValueError('min > max')

    @staticmethod
    def overlap(r1, r2):
        """
        Overlapping rectangles overlap both horizontally & vertically
        """
        Rect.validate_range(r1[0], r1[2])
        Rect.validate_range(r1[1], r1[3])
        Rect.validate_range(r2[0], r2[2])
        Rect.validate_range(r2[1], r2[3])
        return Rect.range_overlap(r1[0], r1[2], r2[0], r2[2]) and Rect.range_overlap(r1[1], r1[3], r2[1], r2[3])


class FeaturesServer:
    def __init__(self):
        self.features = self.read_shapefile_features()

    def read_shapefile_features(self):
        print('Reading features, calculating bboxes...')
        sf = shapefile.Reader("../shapes_files/ne_10m_admin_0_countries")

        field_names = [f[0] for f in sf.fields[1:]]
        name_field_index = field_names.index('NAME')
        assert name_field_index

        features = []

        for s, r in zip(sf.shapes(), sf.records()):
            gi = s.__geo_interface__
            features.append(feature.Feature(gi, str(r[name_field_index])))

        print('Done, features read: ', len(features))
        return features

    def get_features_in_bbox(self, bbox):
        matching_features = [dict(f.__dict__) for f in self.features if Rect.overlap(f.geometry.bbox, bbox)]
        return matching_features
