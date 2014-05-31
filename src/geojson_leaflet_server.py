from bottle import route, run, static_file
import features_server


features = features_server.FeaturesServer()


@route('/')
def server_static():
    return static_file('index.html', root='../html_sample')

@route('/html_sample/<filename>')
def server_static(filename):
    return static_file(filename, root='../html_sample')

@route('/geojson/<zoom:int>/<x:int>/<y:int>.json')
def geojson(zoom, x, y):
    """
    Отдаёт только нужный geojson стран, которые стоят в определённом сегменте карты leаflet
    """
    bbox = features_server.TileUtils.get_tile_bbox(x, y, zoom)
    matching_features = features.get_features_in_bbox(bbox)

    too_close = features_server.TileUtils.degrees_in_pixel(zoom) * 4

    for f in matching_features:
        f['geometry']['coordinates'] = f['geometry'].filter_polygons(too_close)

    print('x: {}, y: {}, bbox: {}, features: {}'.format(x, y, bbox, [f['name'] for f in matching_features]))

    return {
        "type": "FeatureCollection",
        "features": matching_features
    }

@route('/country-geojson/<name>')
def get_country_feature(name):
    return features_server.get_country_feature(name)

run(host='localhost', port=8809)
