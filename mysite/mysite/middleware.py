from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.urls import reverse
import sys
sys.path.append('/mysite/polls')
from polls.models import Choice, Question, Quiz, AnswerSet, Student

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

class TestAlreadyTakenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        print(path)
        if("polls" in path) & (path != "/polls/"):
            parseID  = request.path.split('/')[2:]
            QuizID = int(parseID[0])
            current_user = request.user
            student_to_access = Student.objects.get_or_create(user=current_user)
            possible_student = student_to_access[0]
            possible_student.save()
            quiz_to_access = get_object_or_404(Quiz, pk=QuizID)
            possible_answer_set = AnswerSet.objects.get_or_create(
                student=possible_student,
                quiz=quiz_to_access,
            )
            answer_set = possible_answer_set[0]
            answer_set.save()
            print(answer_set.quiz.quiz_text)
            print(answer_set.score)
            if (answer_set.score != -1):
                print('keylime')
                #to_redirect = '/polls/'+str(answer_set.id)+'/show_results/'
                #return HttpResponseRedirect(to_redirect)
