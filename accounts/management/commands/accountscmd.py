# -*- coding: utf-8 -*-
from django.utils import translation
from django.contrib.auth.models import User
import djclick as click
from logging import getLogger
log = getLogger()

translation.activate('ja')


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.argument('uid')
@click.pass_context
def shop_now(ctx, uid):
    '''Call shop.now '''
    from social_django.utils import load_strategy
    user = User.objects.filter(id=uid).first()
    social = user and user.social_auth.filter(provider='shop').first()
    if not social:
        click.echo('no social user for id {}'.format(uid))
        return
    url = "http://shop.local:8000/accounts/api/now"
    access_token = social.extra_data.get('access_token', '')
    backend = social.get_backend_instance(strategy=load_strategy())
    data = backend.call(url, access_token)
    click.echo(data)
