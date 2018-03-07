from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    #path('<int:quiz_id>/show_results/', views.show_results, name='show_results'),
    #path('<int:answer_set_id>/show_results/', views.show_results, name='show_results'),

    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quizdetail'),
    path('<int:quiz_id>/submit_quiz/', views.submit_quiz, name='submit_quiz'),
    path('<int:answer_set_id>/show_results/', views.show_results, name='show_results'),
]
