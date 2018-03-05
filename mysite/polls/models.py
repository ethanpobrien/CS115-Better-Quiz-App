import datetime

from django.db import models
from django.utils import timezone


# Create your models here.


class Classroom(models.Model):
    classroom_name = models.CharField(max_length=200, default='Classroom Unit')
    classroom_text = models.CharField(max_length=200)

    def __str__(self):
        return self.classroom_name


class Quiz(models.Model):
    title_text = models.CharField(max_length=200, default='quiz title')
    quiz_text = models.CharField(max_length=200)
    number_correct = models.IntegerField(default=0)

    def __str__(self):
        return self.title_text

    #total up number of correct answers
    def totalCorrect(self):
        self.number_correct = 0
        for question in self.question_set.all:
            if question.correct:
                self.number_correct += 1
        self.save()



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    correct = models.BooleanField(default=False)
    correct_answer = models.IntegerField(default=-1)
    selected_answer = models.IntegerField(default=-2)

    def __str__(self):
        return self.question_text

    #find correct answer and save ID for later comparison
    def set_correct_answer(self):
        for choice in self.choice_set.all():
            if choice.correct:
                self.correct_answer = choice.id
        self.save()



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

