# coding: utf-8
from social_core.pipeline.user import create_user as psa_create_user


def create_user(strategy, details, user=None, username=None, *args, **kwargs):
    if not user and username and username != details.get('email', None):
        raise Exception('Email user already exists')

    return psa_create_user(
        strategy, details, user=user, username=username, *args, **kwargs)
