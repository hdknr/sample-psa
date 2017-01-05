# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from corekit import views as core_views
from .forms import AuthConfirmForm

from logging import getLogger
logger = getLogger()


class AuthView(core_views.View):

    @core_views.handler(
        url=r'^login/error',
        name="accounts_login_error", order=20,)
    def error(self, request, ex=None):
        return self.render(
            'accounts/auth/login.error.html', ex=ex)

    @core_views.handler(
        url=r'^login',
        name="accounts_login", order=40,
        decorators=[sensitive_post_parameters(), csrf_protect, never_cache])
    def login(self, request,
              template_name='accounts/auth/login.html', *args, **kwargs):
        return auth_views.login(request, template_name=template_name)

    @core_views.handler(
        url=r'^logout',
        name="accounts_logout", order=40,
        decorators=[auth_views.deprecate_current_app])
    def logout(self, request, *args, **kwargs):
        return auth_views.logout(request, *args, **kwargs)

    @core_views.handler(
        url=r'^confirm/(?P<backend>.+)',
        name="accounts_confirm", order=40,
        decorators=[auth_views.deprecate_current_app])
    def confirm(self, request, backend):
        request.session['agreed'] = False
        form = AuthConfirmForm(request.POST or None)
        if form.is_valid():
            request.session['agreed'] = True
            return self.redirect('social:complete', backend=backend,)
        return self.render(
            'accounts/auth/confirm.html', backend=backend, form=form)


class ProfileView(core_views.View):

    @core_views.handler(
        url=r'^profile',
        name="accounts_profile_index", order=40,
        decorators=[core_views.View.requires('login')])
    def index(self, request, *args, **kwargs):
        return self.render(
            'accounts/profile/index.html', user=request.user)
