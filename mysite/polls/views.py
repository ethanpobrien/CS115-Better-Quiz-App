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

#added to test submitting multiple forms with one button
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
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    current_student.save()

    answerset = get_object_or_404(AnswerSet, pk=answer_set_id)
    #get quiz
    quiz = get_object_or_404(Quiz, pk=answerset.quiz.id)

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
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    current_student.save()

    #use student and quiz objects to get or create an answer set
    possible_answer_set = AnswerSet.objects.get_or_create(
        student = current_student, 
        quiz=question.quiz,
    )
    answer_set = possible_answer_set[0]
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
        selected_choice.votes += 1
        selected_choice.save()

        for set_choice in answer_set.answers.all():
            if set_choice.question == question:
                answer_set.answers.remove(set_choice)

        answer_set.answers.add(selected_choice)
        answer_set.update_score()
        answer_set.save()

    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))



#def submit_quiz(request, answer_set_id):
def submit_quiz(request, quiz_id):
    current_user = request.user
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    #current_student is what we want
    current_student.save()

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    #use student and quiz objects to get or create an answer set
    possible_answer_set = AnswerSet.objects.get_or_create(
        student = current_student, 
        quiz=quiz,
    )
    answer_set = possible_answer_set[0]
    answer_set.save()

    
    #right now, pushes through to command line where runserver was used
    #shows correct selections inside the post data...
    if request.method == 'POST':
        post_obj = request.POST
        #print(list(post_obj.items()))
        post_dict = post_obj.dict()

        #dict_list = post_dict.items()
        #sliced_dict_list = dict_list[1:]

        #clears any choices
        for set_choice in answer_set.answers.all():
            answer_set.answers.remove(set_choice)
            answer_set.save()

        #this prints key, value pairs from the dict, and it lists question.id, choice.id
        #and also the CSRF token right at the start... just skip with slicing?
        for k, v in post_dict.items():
            print(k, v)
            #print(type(k))
            #print(int(k, base=10))
            #if type(k) == int:
            if k != 'csrfmiddlewaretoken':
                for question in quiz.question_set.all():
                    print('k = ', k)
                    #print('k = ', int(k))
                    print('question.id = ', question.id)
                    if int(k) == question.id:
                        print('inside if loop lol')
                        print(k)
                        answer = Choice.objects.get(pk=v) 
                        answer_set.answers.add(answer)



                        answer_set.update_score()
                        answer_set.save()







    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))
    #try:
        # retrieve selected choice's model
        #selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #except (KeyError, Choice.DoesNotExist):
        #return render(request, 'polls/detail.html', {
            #'question': question,
            #'error_message': "You didn't select a choice.",
        #})
    #else:
        #selected_choice.votes += 1
        #selected_choice.save()

        #for set_choice in answer_set.answers.all():
            #if set_choice.question == question:
                #answer_set.answers.remove(set_choice)

        #answer_set.answers.add(selected_choice)
        #answer_set.update_score()



    #answer_set.save()

