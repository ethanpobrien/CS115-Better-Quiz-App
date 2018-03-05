from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login

from .models import Choice, Question, Quiz

'''
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
            login(request, user)
            # Redirect to success page
'''


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


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #pull up question model. Update correct answers
        question.set_correct_answer()
        #retrieve selected choice's model
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #update vote count
        selected_choice.votes += 1
        #if correct, set question to correct
        if selected_choice.id == question.correct_answer:
            question.correct = True
        #update server with response
        selected_choice.save()
        question.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.quiz.id,)))
