# coding: utf-8
from social_core.pipeline.user import create_user as psa_create_user
from social_core.pipeline.partial import partial


def create_user(strategy, details, backend, user=None, username=None,
                *args, **kwargs):
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
        return AuthView(strategy.request).confirm(
            strategy.request, backend=backend.name)
