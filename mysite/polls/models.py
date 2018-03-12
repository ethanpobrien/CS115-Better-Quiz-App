import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


#one to one with User, should hold unique student models.
#Don't directly act on User, just on Student?
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

    #classmethod to create new student from user
    @classmethod
    def create(cls, user):
        student = cls(user=user)
        return student


class Course(models.Model):
    subject = models.CharField(max_length=200)
    course_description = models.CharField(max_length=200)
    students = models.ManyToManyField(Student)
    size = models.IntegerField(default=0)

    def __str__(self):
        #return self.classroom_name
        return self.subject

    def update_size(self):
        self.size = 0
        for student in self.students.all:
            self.size += 1
        self.save()


class Teacher(models.Model):
    #if teacher, can access uuser
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE) 

    def __str__(self):
        return self.user.username


class Quiz(models.Model):
    title_text = models.CharField(max_length=200)
    quiz_text = models.CharField(max_length=200)
    number_correct = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title_text

    class Meta:
        #changes to plural form if more than one
        verbose_name = 'Better Quiz'
        verbose_name_plural = 'Better Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    #If the user answers correctly, hence false default
    correct = models.BooleanField(default=False)
    #always!! contains ID of choice with .correct = True
    correct_answer = models.IntegerField(default=-1)
    selected_answer = models.IntegerField(default=-2)

    def __str__(self):
        return self.question_text

    #find correct answer and save ID for later comparison
    #will take most recently selected choice as correct
    def set_correct_answer(self):
        for choice in self.choice_set.all():
            if choice.correct:
                self.correct_answer = choice.id
        self.save()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #answer_set = models.ManyToManyField(AnswerSet)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class AnswerSet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=-1)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=-1)
    answers = models.ManyToManyField(Choice)
    score = models.IntegerField(default=-1)
    #percent correct
    grade = models.DecimalField(max_digits=4, decimal_places=2)

    def update_score(self):
        self.score = 0
        for choice in self.answers.all():
            if choice.correct == True:
                self.score += 1
        self.save()

    def update_grade(self):
        count = 0
        for q in self.quiz.question_set.all():
            count += 1
        self.update_score()
        score = self.score
        self.grade = float(score/count)
        self.save()


#class ClassAnswerSet(models.Model):
class ClassQuizResults(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=-1)
    #fields that I want to be able to see in HTML at some point
    #average is total class average, ie sum of individual scores/count
    average = models.IntegerField(default=0)
    #median score
    median = models.IntegerField(default=0)
    #std dev
    std_dev = models.IntegerField(default=0)
    low_grade = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    high_grade = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    #iterable of all answer sets for some quiz
    #returns highest score (as percent)
    def get_high(self):
        high = 0
        for answer_set in AnswerSet.objects.all().filter(quiz=self.quiz):
            answer_set.update_grade()
            if answer_set.grade > high:
                high = answer_set.grade

        self.high_grade = high
        self.save()

    #returns lowest score (as percent)
    def get_low(self):
        low = 1000
        for answer_set in AnswerSet.objects.all().filter(quiz=self.quiz):
            answer_set.update_grade()
            if answer_set.grade < low:
                low = answer_set.grade

        self.low_grade = low
        self.save()

    #returns average score (as percent)
    def set_average(self):
        self.average = 0
        sum_grades = 0
        count = 0
        for answer_set in AnswerSet.objects.all().filter(quiz=self.quiz):
            answer_set.update_grade()
            sum_grades += answer_set.grade
            count += 1
        self.average = sum_grades/count
        self.save()