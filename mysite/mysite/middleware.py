from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    #ensures user is logged in before trying to access anything
    def process_request(self, request):
        ##if user not authenticated then perform middleware
        if not request.user.is_authenticated:
            ##takes in current path as string
            path = request.path_info
            # if path is not admin or account, redirect if not logged in.
            #store any non-userlocked sites in redirect_ignore
            redirect_ignore = ["admin", "account"]
            if not any (category in path for category in redirect_ignore):
                return HttpResponseRedirect("/accounts/login/")

class PageNotFoundMiddleware(MiddlewareMixin):
    #basic redirects to prevent unwanted access
    def process_request(self, request):
            path = request.path_info
            # if path is not admin, account, or polls, redirect if not logged in.
            redirect_ignore = ["admin", "account", "polls"]
            if not any (category in path for category in redirect_ignore):
                if not request.user.is_authenticated:
                    return HttpResponseRedirect("/accounts/login/")
                else:
                    return HttpResponseRedirect("/polls/")
