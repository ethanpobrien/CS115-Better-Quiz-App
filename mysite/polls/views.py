from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login

from .models import Choice, Question, Quiz, Student, AnswerSet

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


def show_results(request, answer_set_id):
    #get user
    current_user = request.user

    #get student object from user object
    possibly_student = Student.objects.get_or_create(user=current_user)
    current_student = possibly_student[0]
    current_student.save()

    answerset = get_object_or_404(AnswerSet, pk=answer_set_id)

    #get quiz
    quiz = get_object_or_404(Quiz, pk=answerset.quiz.id)


    #get quiz answer set
    #possible_answer_set = AnswerSet.objects.get_or_create(
    #answer_set = AnswerSet.objects.get_or_create(
        #student = current_student, 
        #quiz=quiz,
    #)
    #answer_set = possible_answer_set[0]
    #answer_set.save()
    answerset.save()
    


    return render(request, 'polls/show_results.html', {
        'quiz': quiz,
        'answerset': answerset,
        'answer_set_id': answerset.id,
        })





#changed to add some things to the answerset selections, seems to be working by looking
#at the sqlite3 database and tables in it
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    #trying to pull the user id to get the AnswerSet for them and the quiz
    current_user = request.user
    #get student object from user object
    possibly_student = Student.objects.get_or_create(user=current_user)
    current_student = possibly_student[0]
    current_student.save()

    #use student and quiz objects to get or create an answer set
    answerset_tuple = AnswerSet.objects.get_or_create(
        student = current_student, 
        quiz=question.quiz,
    )
    answer_set = answerset_tuple[0]
    answer_set.save()
    

    try:
        # pull up question model. Update correct answers
        question.set_correct_answer()

        # retrieve selected choice's model
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # update vote count
        selected_choice.votes += 1

        # if correct, set question to correct
        if selected_choice.id == question.correct_answer:
            question.correct = True
        else:
            question.correct = False
        ## update server with response
        selected_choice.save()
        question.save()

        #not necessary to have correct check, as we alse want to 
        #   record incorrect answers 
        #
        #if selected_choice.correct == True:

        answer_set.answers.add(selected_choice)
        answer_set.save()


    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))

