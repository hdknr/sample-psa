# coding:utf-8
'''
http://python-social-auth.readthedocs.io/en/latest/backends/implementation.html     # NOQA
'''

from social_core.backends.oauth import BaseOAuth2


class ShopOAuth2(BaseOAuth2):
    '''Shop OAuth authentication backend'''
    name = 'shop'
    AUTHORIZATION_URL = 'http://shop.local:8000/accounts/o/authorize/'
    ACCESS_TOKEN_URL = 'http://shop.local:8000/accounts/o/token/'
    SCOPE_SEPARATOR = ','

    # user_data converter
    EXTRA_DATA = [
        ('user_id', 'id'),
        ('expires_in', 'expires'),
        ('endpoint_name', 'endpoint_name'),
    ]

    ACCESS_TOKEN_METHOD = 'POST'
    USER_URL = 'http://shop.local:8000/accounts/api/profile/'
    ID_KEY = 'user_id'          # Ship User key

    def get_user_details(self, response):
        # API: required to implement.
        return response

    def user_data(self, access_token, *args, **kwargs):
        # OAuth2 Resource Endpoint
        return self.call(self.USER_URL, access_token, *args, **kwargs)

    def call(self, endpoint, access_token, headers={}, *args, **kwargs):
        headers['Authorization'] = 'Bearer {0}'.format(access_token)
        response = self.get_json(endpoint, headers=headers)
        return response
