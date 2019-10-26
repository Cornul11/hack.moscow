import json
import requests


class Point(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class BoundingBox(object):
    def __init__(self, top_left_point: Point, bottom_right_point: Point):
        self.top_left_point = top_left_point
        self.bottom_right_point = bottom_right_point

    def get_at_param(self):
        return '{},{},{},{}'.format(
            self.top_left_point.lat, self.top_left_point.lon,
            self.bottom_right_point.lat, self.bottom_right_point.lon
        )


def get_signature(app_id, app_code):
    signature_url = 'http://signature.venue.maps.api.here.com'
    uri = signature_url+'/venues/signature/v1'

    params = {
        'app_id': app_id,
        'app_code': app_code
    }
    response = requests.get(uri, params=params)
    assert response.status_code == 200
    return response.json()


def get_all_venues(app_id, app_code, signature, policy, key_pair_id):
    # todo: add random: 1-4
    all_venues_url = 'http://static-1.venue.maps.api.here.com'
    uri = all_venues_url+'/1/models-full/index_bb.json'

    params = {
        'app_id': app_id,
        'app_code': app_code,
        'Signature': signature,
        'Policy': policy,
        'Key-Pair-Id': key_pair_id
    }

    response = requests.get(uri, params=params)
    assert response.status_code == 200
    return response.json()


def discovery_venue(app_id, app_code, bb: BoundingBox):
    venue_url = 'https://indoor-discovery.venue.maps.api.here.com'
    uri = venue_url+'/discovery/v2'

    params = {
        'app_id': app_id,
        'app_code': app_code,
        'at': bb.get_at_param()
    }

    response = requests.get(uri, params=params)
    assert response.status_code == 200
    return response.json()


def get_full_model(app_id, app_code, signature, policy, key_pair_id, venue_id):
    venue_url = 'http://static-1.venue.maps.api.here.com'
    uri = venue_url+'/1/models-full/{venue_id}.json'.format(venue_id=venue_id)

    params = {
        'app_id': app_id,
        'app_code': app_code,
        'Signature': signature,
        'Policy': policy,
        'Key-Pair-Id': key_pair_id
    }

    response = requests.get(uri, params=params)
    assert response.status_code == 200
    print(response.json())
    return response.json()
