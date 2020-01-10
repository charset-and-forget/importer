import copy
# import json

import requests


class ApiError(Exception):
    pass


class ApiValidationError(ApiError):
    pass


class SectionStatus:
    PRIVATE = 1
    PUBLIC = 2
    UNLISTED = 3


class ApiBase:
    API_VERSION = '1.3'

    def __init__(self, domain, api_key, http_auth_user=None, http_auth_pwd=None, verbosity=0):
        self.domain = domain
        self.api_key = api_key
        self.verbosity = verbosity
        self.auth = (http_auth_user, http_auth_pwd) if http_auth_user else None

    def _request(self, request):
        # requests.Request(method, url, headers, files, data, params, auth, cookies, hooks, json)
        self._print_info_about_request(request)
        session = requests.Session()
        prepped = request.prepare()
        response = session.send(prepped)
        self._print_info_about_response(response)
        if response.status_code == requests.codes.ok:
            return response.json()
        print(response.url)
        print(response.history)
        raise ApiError(response.json())

    def _print_info_about_request(self, request):
        if self.verbosity == 0:
            return
        if self.verbosity >= 1:
            print('API call:', request.method, request.url)
        if self.verbosity >= 2:
            print('params:', request.params)
            print('json:', request.json)
        # print()

    def _print_info_about_response(self, response):
        if self.verbosity == 0:
            return
        if self.verbosity >= 1:
            print('API response:', response.status_code)
        if self.verbosity >= 2:
            if response.status_code != requests.codes.ok or self.verbosity >= 3:
                print(response.content)
        print()

    def _get_request(self, url, params=None):
        params = self._build_params(params)
        request = requests.Request(
            'GET',
            url=url,
            params=params,
            auth=self.auth,
        )
        return self._request(request)

    def _post_request(self, url, params=None, data=None):
        params = self._build_params(params)
        request = requests.Request(
            'POST',
            url=url,
            json=data,
            params=params,
            auth=self.auth,
        )
        return self._request(request)

    def _put_request(self, url, params=None, data=None):
        params = self._build_params(params)
        request = requests.Request(
            'PUT',
            url=url,
            params=params,
            json=data,
            auth=self.auth,
        )
        return self._request(request)

    def _build_params(self, params):
        params = copy.deepcopy(params) if params else {}
        params['api_key'] = self.api_key
        return params


class API(ApiBase):
    def upload_image(self, image_url, caption='', credit='', alt=''):
        url = 'https://{}/api/{}/images'.format(self.domain, self.API_VERSION)
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

    def get_sections(self):
        api_url = 'https://{}/api/{}/sections'.format(self.domain, self.API_VERSION)
        response = self._get_request(api_url)
        return map(self._extract_section_info_from_item, response)

    def create_section(self, title, url, status=SectionStatus.PRIVATE, about_html=''):
        api_url = 'https://{}/api/{}/sections'.format(self.domain, self.API_VERSION)
        params = {
            'title': title,
            'url': url,
            'status': status,
            'about_html': about_html,
        }
        response = self._post_request(api_url, data=params)
        return self._extract_section_info_from_item(response)

    def create_draft(self, **entry):
        api_url = 'https://{}/api/{}/drafts'.format(self.domain, self.API_VERSION)
        if not entry.get('headline'):
            raise ApiValidationError('headline is required')
        return self._post_request(api_url, data=entry)

    def publish_draft(self, draft_id):
        api_url = 'https://{}/api/{}/drafts/{}'.format(self.domain, self.API_VERSION, draft_id)
        return self._put_request(api_url, data={'action': 'publish'})

    def create_author(
        self,
        email,
        name,
        first_name=None,
        last_name=None,
        password=None,
        about_html='',
        image_id=None,
        specific_data=None,
    ):
        # api_url = 'https://{}/api/{}/authors'.format(self.domain, self.API_VERSION)
        api_url = 'https://{}/api/1.1/authors'.format(self.domain)
        params = {
            'email': email,
            'name': name,
            'about_html': about_html,
        }
        if first_name:
            params['first_name'] = first_name
        if last_name:
            params['last_name'] = last_name
        if password:
            params['password'] = password
        if image_id:
            params['image_id'] = image_id
        if image_id:
            params['image_id'] = image_id
        if specific_data:
            params['specific_data'] = specific_data
        response = self._post_request(api_url, data=params)
        return response

    def _extract_section_info_from_item(self, item):
        return {
            'id': item['id'],
            'title': item['title'],
            'url': item['url'],
            'status': item['status'],
            'parent_id': item['parent_id'],
        }
