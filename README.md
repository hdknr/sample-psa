# sample-psa
Python Social Auth Sample 

## social-app-django

- https://github.com/python-social-auth/social-app-django
- https://github.com/python-social-auth/social-core
- http://python-social-auth.readthedocs.io/en/latest/configuration/django.html



## settings.AUTHENTICATION_BACKENDS

- django default(1.10.4):

~~~py
In [1]: from django.conf import global_settings

In [2]: global_settings.AUTHENTICATION_BACKENDS
Out[2]: [u'django.contrib.auth.backends.ModelBackend']
~~~

~~~py
from django.conf import global_settings
AUTHENTICATION_BACKENDS = [
    'social.backends.facebook.FacebookOAuth2',
] + global_settings.AUTHENTICATION_BACKENDS
~~~
