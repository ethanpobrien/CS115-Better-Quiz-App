from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quizdetail'),

    path('<int:quiz_id>/submit_quiz/', views.submit_quiz, name='submit_quiz'),
    path('<int:answer_set_id>/show_results/', views.show_results, name='show_results'),

    path('answerset/<int:pk>/', views.AnswerSetView.as_view(), name='answer_set_view'),
    
    path('classresults/', views.ClassQuizResultsView.as_view(), name='classquizresultsview'),
    path('<int:classquizresults_id>/classquizresults/', views.classquizresults, name='classquizresults'),

    path('edit_info/', views.edit_info, name='edit_info'),
    path('enter_info/', views.enter_info, name='enter_info'),
]
