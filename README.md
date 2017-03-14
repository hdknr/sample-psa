# sample-psa

Python Social Auth Sample

## social-app-django

- https://github.com/python-social-auth/social-app-django
- https://github.com/python-social-auth/social-core
- http://python-social-auth.readthedocs.io/en/latest/configuration/django.html



## Django default settings.AUTHENTICATION_BACKENDS

django default(1.10.4):

~~~py
In [1]: from django.conf import global_settings

In [2]: global_settings.AUTHENTICATION_BACKENDS
Out[2]: [u'django.contrib.auth.backends.ModelBackend']
~~~


## Facebook

settings.py:

~~~py
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
] + global_settings.AUTHENTICATION_BACKENDS

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',
]
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
from app.psa import *       # NOQA Facebook
~~~

psa.py:

~~~py
'''
Facebook
http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2
'''
SOCIAL_AUTH_FACEBOOK_KEY = "{{ set key }}"
SOCIAL_AUTH_FACEBOOK_SECRET = "{{ set secret }}"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email',
}
~~~

accounts/urls.py:

~~~py
from django.conf.urls import url, include
from . import views

'''
auth request: /accounts/social/login/facebook/?next=%2Faccounts%2Fprofile
auth response: /accounts/social/complete/facebook/?redirect_state={{ state }}&code={{ oauth code}}&state={{ oauth state }}
'''
urlpatterns = [
    url('^social/', include('social_django.urls', namespace='social')),
] + views.AuthView.urls() + views.ProfileView.urls()
~~~

accounts/templates/accounts/auth/login.html:

~~~html
<a href="{% url 'social:begin' backend='facebook'  %}?{{ request.GET.urlencode }}">
  {% trans 'Facebook Login' %}
</a>
~~~

## Exception

settings.py:

~~~py
MIDDLEWARE += [
    'accounts.middleware.AccountMiddleware',
]
~~~

accounts/middleware.py:

~~~py
from social_django.middleware import SocialAuthExceptionMiddleware


class AccountMiddleware(SocialAuthExceptionMiddleware):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        from accounts.views import AuthView
        return super(AccountMiddleware, self).process_exception(
            request, exception) or AuthView(request).error(request, exception)
~~~

# Partial pipeline for UI interaction.

customized strategy for Django:

- replacing `create_user`
- append `confirm` for UI interaction

~~~py
from social_django.strategy import DjangoStrategy
from corekit.views import View


class Strategy(DjangoStrategy):

    def get_pipeline(self, backend=None):
        ''' override to modify piplines'''
        replace = {
            'social_core.pipeline.user.create_user': 'accounts.pipeline.create_user',   # NOQA
        }
        res = super(Strategy, self).get_pipeline(backend=backend)
        return tuple(replace.get(i, i) for i in res) + (
            'accounts.pipeline.confirm', )
~~~

settings.py:

~~~py
SOCIAL_AUTH_STRATEGY = 'accounts.strategy.Strategy'
~~~

accounts/pipeline.py:

~~~py
from social_core.pipeline.user import create_user as psa_create_user
from social_core.pipeline.partial import partial


def create_user(strategy, details, backend, user=None, username=None,
                *args, **kwargs):

    # duplicated email are banned.
    if not user and username and username != details.get('email', None):
        raise Exception('Email user already exists')

    return psa_create_user(
        strategy, details, backend=backend, user=user,
        username=username, *args, **kwargs)


@partial
def confirm(strategy, details, backend, user=None, username=None,
            pipeline_index=None, *args, **kwargs):

    from accounts.views import AuthView
    if not strategy.session_get('agreed'):
        # if not agreed by the User, UI is provided.
        return AuthView(strategy.request).confirm(
            strategy.request, backend=backend.name)
~~~            

accounts/views.py:

~~~py
class AuthView(core_views.View):

    @core_views.handler(
        url=r'^confirm/(?P<backend>.+)',
        name="accounts_confirm", order=40,
        decorators=[auth_views.deprecate_current_app])
    def confirm(self, request, backend):
        request.session['agreed'] = False
        form = AuthConfirmForm(request.POST or None)
        if form.is_valid():
            # Agreed by User, back to the pipeline.
            request.session['agreed'] = True
            return self.redirect('social:complete', backend=backend,)
        return self.render(
            'accounts/auth/confirm.html', backend=backend, form=form)
~~~            

# Custom OAuth2 Provider

define `social_core.backends.oauth.BaseOAuth2` backend class:

~~~py
from social_core.backends.oauth import BaseOAuth2


class ShopOAuth2(BaseOAuth2):
    ...
~~~

add the backend to `AUTHENTICATION_BACKENDS`

~~~py
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'app.providers.ShopOAuth2',
] + global_settings.AUTHENTICATION_BACKENDS
~~~

login template:

~~~html
<a href="{% url 'social:begin' backend='shop'  %}?{{ request.GET.urlencode }}">
    {% trans 'Shop Login' %} 
</a>
~~~

