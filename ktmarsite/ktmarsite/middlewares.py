from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class CheckUserIsBlockedMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_active:
                logout(request)
                return HttpResponseRedirect('/')