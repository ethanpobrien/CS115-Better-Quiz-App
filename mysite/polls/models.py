import datetime

from django.db import models
from django.utils import timezone

class Quiz(models.Model):
    title_text = models.CharField(max_length=200, default='quiz title')
    quiz_text = models.CharField(max_length=200)
    def __str__(self):
        return self.title_text

# Create your models here.
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    correct = models.BooleanField(default=False)
    def __str__(self):
      return self.question_text
    def was_published_recently(self):
      now = timezone.now()
      return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
