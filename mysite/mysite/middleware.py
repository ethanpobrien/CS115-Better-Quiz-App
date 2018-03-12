from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import sys
sys.path.append('/mysite/polls')
from ..polls.models import Choice, Question, Quiz, AnswerSet, Student


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

class TestAlreadyTakenMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if("polls" in path):
            polls, QuizID  = request.path.split('/')[-1:]
            current_user = request.user
            student = Student.objects.get_or_create(user=current_user)
            quiz = get_object_or_404(Quiz, pk=QuizID)
            possible_answer_set = AnswerSet.objects.get_or_create(
                student=student,
                quiz=quiz,
            )
            answer_set = possible_answer_set[0]
            if answer_set.score != -1:
                return HttpResponseRedirect('/polls/<int:answer_set_id>/show_results/')