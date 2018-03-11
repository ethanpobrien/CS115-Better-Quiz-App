from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import Choice, Question, Quiz, Student, AnswerSet




class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        return Quiz.objects.all()


class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Quiz.objects.all()


# added to test submitting multiple forms with one button
class QuizDetailView(generic.DetailView):
    model = Quiz
    template_name = 'polls/quizdetail.html'

    def get_queryset(self):
        return Quiz.objects.all()


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'polls/results.html'


def show_results(request, answer_set_id):
    #get user
    current_user = request.user
    #get student object from user object
    print(current_user.id)
    print('codeWWORKSSSSSSSSSSSSSSSSSSSSSSSSS')
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    current_student.save()
    answerset = get_object_or_404(AnswerSet, pk=answer_set_id)
    # get quiz
    quiz = get_object_or_404(Quiz, pk=answerset.quiz.id)
    answerset.save()
    return render(request, 'polls/show_results.html', {
        'quiz': quiz,
        'answerset': answerset,
        'answer_set_id': answerset.id,
    })


# def submit_quiz(request, answer_set_id):
def submit_quiz(request, quiz_id):
    current_user = request.user
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    # current_student is what we want
    current_student.save()
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # use student and quiz objects to get or create an answer set
    possible_answer_set = AnswerSet.objects.get_or_create(
        student=current_student,
        quiz=quiz,
    )
    answer_set = possible_answer_set[0]

    # right now, pushes through to command line where runserver was used
    # shows correct selections inside the post data...

    if request.method == 'POST':
        post_obj = request.POST
        # print(list(post_obj.items()))
        post_dict = post_obj.dict()

        # dict_list = post_dict.items()
        # sliced_dict_list = dict_list[1:]

        # clears any choices
        for set_choice in answer_set.answers.all():
            answer_set.answers.remove(set_choice)
            answer_set.save()

        # this prints key, value pairs from the dict, and it lists question.id, choice.id
        # and also the CSRF token right at the start... just skip with slicing?
        for k, v in post_dict.items():
            print(k, v)
            # print(type(k))
            # print(int(k, base=10))
            # if type(k) == int:
            if k != 'csrfmiddlewaretoken':
                for question in quiz.question_set.all():
                    print('k = ', k)
                    # print('k = ', int(k))
                    print('question.id = ', question.id)
                    if int(k) == question.id:
                        print('inside if loop lol')
                        print(k)
                        answer = Choice.objects.get(pk=v)
                        answer_set.answers.add(answer)

                        answer_set.update_score()
                        answer_set.save()

    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))

def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def handler500(request, template_name='500.html'):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
