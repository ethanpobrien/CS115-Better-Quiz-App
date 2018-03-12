from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import sys
sys.path.append('/mysite/polls/')
from polls.models import Choice, Question, Quiz, AnswerSet, Student
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import resolve
from django.urls import reverse
from polls import views
from polls import urls 


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


class TestAlreadyTakenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        res = resolve(request.path)
        print('call res')
        print(res)
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        res = resolve(request.path)
        user = request.user
        if res.url_name == 'detail':
            quiz_id = res.kwargs
            quiz = Quiz.objects.get(pk=quiz_id['pk'])
            student = Student.objects.get(user=user)
            sets = AnswerSet.objects.all().filter(student=student, quiz=quiz)
            if not sets:
                return None
            else:
                answer_set = sets[0]
                print(answer_set)
                print(answer_set.answers.count())
                print(quiz.question_set.count())
                if answer_set.answers.count() == quiz.question_set.count():
                    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))

