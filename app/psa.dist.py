# Facebook
# http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2
SOCIAL_AUTH_FACEBOOK_KEY = "{{ set key }}"
SOCIAL_AUTH_FACEBOOK_SECRET = "{{ set secret }}"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email',
}


# Shop
SOCIAL_AUTH_SHOP_KEY = "{{ set key }}"
SOCIAL_AUTH_SHOP_SECRET = "{{ set secret }}"
SOCIAL_AUTH_SHOP_SCOPE = ['email']
SOCIAL_AUTH_SHOP_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email',
}
