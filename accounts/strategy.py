# coding: utf-8
from social_django.strategy import DjangoStrategy


class Strategy(DjangoStrategy):

    def get_pipeline(self, backend=None):
        replace = {
            'social_core.pipeline.user.create_user': 'accounts.pipeline.create_user',   # NOQA
        }
        res = super(Strategy, self).get_pipeline(backend=backend)
        return (replace.get(i, i) for i in res)
