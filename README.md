# sample-psa
Python Social Auth Sample

## social-app-django

- https://github.com/python-social-auth/social-app-django
- https://github.com/python-social-auth/social-core
- http://python-social-auth.readthedocs.io/en/latest/configuration/django.html



## Django default settings.AUTHENTICATION_BACKENDS

- django default(1.10.4):

~~~py
In [1]: from django.conf import global_settings

In [2]: global_settings.AUTHENTICATION_BACKENDS
Out[2]: [u'django.contrib.auth.backends.ModelBackend']
~~~


## Facebook

- settings.py

~~~py
AUTHENTICATION_BACKENDS = [
    'social.backends.facebook.FacebookOAuth2',
] + global_settings.AUTHENTICATION_BACKENDS

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
]
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
from app.psa import *       # NOQA Facebook
~~~

- psa.py

~~~py
# Facebook
# http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2
SOCIAL_AUTH_FACEBOOK_KEY = "{{ set key }}"
SOCIAL_AUTH_FACEBOOK_SECRET = "{{ set secret }}"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email',
}
~~~

- accounts/urls.py

~~~py
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

# auth request: /accounts/social/login/facebook/?next=%2Faccounts%2Fprofile
# auth response: /accounts/social/complete/facebook/?redirect_state={{ state }}&code={{ oauth code}}&state={{ oauth state }}
urlpatterns = [
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
] + views.AuthView.urls() + views.ProfileView.urls()
~~~

- accounts/templates/accounts/auth/login.html

~~~html
<a href="{% url 'social:begin' backend='facebook'  %}?{{ request.GET.urlencode }}">
  {% trans 'Facebook Login' %}
</a>
~~~
