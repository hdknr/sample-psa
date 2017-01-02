# coding: utf-8
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
