import os


API = {
    'domain': os.getenv('DOMAIN'),
    'api_key': os.getenv('API_KEY'),
    'http_auth_user': os.getenv('HTTP_AUTH_USER'),
    'http_auth_pwd': os.getenv('HTTP_AUTH_PWD'),
    'rate_limit': int(os.getenv('API_RATE_LIMIT')),
    'verbosity': 0,
}
