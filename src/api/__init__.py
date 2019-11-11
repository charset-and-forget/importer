import copy
import json

import requests


class ApiError(Exception):
    pass


class API:
    API_VERSION = 'v1.3'
    API_URL = 'https://www.rebelmouse.com/api'

    def __init__(self, api_key):
        self.api_key = api_key

    def upload_image(self, image_url, caption, credit, alt):
        url = '{}/{}/images'.format(self.API_URL, self.API_VERSION)
        params = {
            'image_url': image_url,
            'caption': caption,
            'photo_credit': credit,
            'alt': alt,
        }
        response = self._post_request(url, data=params)
        result = {
            'is_animated_gif': response['is_animated_gif'],
            'shortcode_id': response['shortcode_id'],
            'image_id': response['id'],
            'shortcode': response['shortcode'],
        }
        return result

    def _request(self, request):
        # requests.Request(method, url, headers, files, data, params, auth, cookies, hooks, json)
        session = requests.Session()
        prepped = request.prepare()
        response = session.send(prepped)
        if response.status_code == requests.codes.ok:
            return response.json()
        raise ApiError(response.json())

    def _post_request(self, url, params=None, data=None):
        params = self._build_params(params)
        request = requests.Request(
            'POST',
            url=url,
            data=json.dumps(data),
            params=params,
        )
        return self._request(request)

    def _build_params(self, params):
        params = copy.deepcopy(params) if params else {}
        params['api_key'] = self.api_key
        return params
