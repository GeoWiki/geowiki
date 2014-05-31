
class Geometry(dict):
    """
    Геометрия в смысле шейпфайла, фигура на карте.
    """
    def __init__(self, geo_interface):
        super().__init__(**geo_interface)
        self.type = geo_interface['type']
        self.coordinates = geo_interface['coordinates']
        self.bbox = self.__calc_bbox()

    def __calc_bbox(self):
        bbox = [180, 90, -180, -90]
        for polygons in self.__get_polygons():
            for polygon in polygons:
                for p in polygon:
                    if p[0] < bbox[0]:
                        bbox[0] = p[0]
                    if p[0] > bbox[2]:
                        bbox[2] = p[0]
                    if p[1] < bbox[1]:
                        bbox[1] = p[1]
                    if p[1] > bbox[3]:
                        bbox[3] = p[1]

        assert bbox[0] < bbox[2]
        assert bbox[1] < bbox[3]
        return bbox


    def __get_polygons(self):
        if self['type'] == 'MultiPolygon':
            return self['coordinates']
        elif self['type'] == 'Polygon':
            return [self['coordinates']]
        else:
            raise ValueError('Not implemented yet')

    @staticmethod
    def too_close(p1, p2, delta):
        return abs(p1[0]-p2[0]) < delta and abs(p1[1]-p2[1]) < delta

    def filter_polygons(self, delta):
        """
        Удаляет вроде как лишние (слишком близкие) точки.
        TODO: написать тест.
        """
        result_multi_polygons = []
        for polygons in self.__get_polygons():
            result_polygons = []
            for polygon in polygons:
                result_polygon = []

                if len(polygon) == 1:
                    print('1-poly')

                for p in polygon:
                    if not result_polygon or not Geometry.too_close(p, result_polygon[-1], delta):
                        result_polygon.append(p)

                print('{} filtered for distance of {} degrees. Points before: {}, after: {}'
                      .format(self['type'], delta, len(polygon), len(result_polygon)))

                if len(result_polygon) > 1:
                    result_polygons.append(result_polygon)

            result_multi_polygons.append(result_polygons)

        return result_multi_polygons


class Feature:
    def __init__(self, geo_interface, name):
        self.geometry = Geometry(geo_interface)
        self.type = "Feature"
        self.id = name
        self.name = name
        self.properties = {
            "name": name
        }
