from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import sys
sys.path.append('/mysite/polls')
from polls.models import Choice, Question, Quiz, AnswerSet, Student
from django.contrib import messages
from django.contrib.messages import get_messages


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
    #checks if quiz already taken. If taken already, redirect to results.
    def process_request(self, request):
        path = request.path_info
        #print(path)

        #only perform action if they're about to try to take quiz.
        #if("polls" in path) & (path != "/polls/") & ('results' not in path):

        if("polls" in path) & (path != "/polls/") & ('results' not in path) & ('edit_info' not in path) & ('enter_info' not in path):

            #get quiz id from url
            parseID  = request.path.split('/')[2:]
            QuizID = int(parseID[0])

            #get current user's answerset
            current_user = request.user
            student = get_object_or_404(Student, user=current_user)

            quiz = get_object_or_404(Quiz, pk=QuizID)
            tuple_answer_set = AnswerSet.objects.get_or_create(
                    student=student,
                    quiz=quiz,
                    grade=0,
                    )
            answer_set = tuple_answer_set[0]

            #return render(request, 'polls/detail.html', {'quiz':quiz, 'student':student})
            
            #logic from views
            post_obj = request.POST
            post_dict = post_obj.dict()

            #number of quiz questions
            num_questions = quiz.question_set.count()

            #make this a clearchoices function in answerset
            for set_choice in answer_set.answers.all():
                answer_set.answers.remove(set_choice)
                answer_set.save()

            if len(post_dict) < num_questions + 1:
                messages.add_message(request, 30, 'You cannot submit a quiz unless you have answered every question')
                print(messages)
                for k, v in post_dict.items():
                    if k != 'csrfmiddlewaretoken':
                        for question in quiz.question_set.all():
                            if int(k) == question.id:
                                answer = Choice.objects.get(pk=v)
                                answer.votes += 1
                                answer.save()

                                answer_set.answers.add(answer)
                                answer_set.update_score()


                return render(request,'polls/detail.html',{
                    'quiz': quiz,
                    'answerset': answer_set,
                    })

            
            if answer_set.score == -1:
                return render(request,'polls/detail.html',{
                    'quiz': quiz,
                    'answerset': answer_set,
                    })

