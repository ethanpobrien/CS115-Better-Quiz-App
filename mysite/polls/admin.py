from django.contrib import admin

from .models import Choice, Question, Quiz, AnswerSet


class ChoiceInline(admin.TabularInline):
    readonly_fields = ('votes',)
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    #readonly_fields = ('pub_date',)
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    
    inlines = [ChoiceInline]

    list_display = ['question_text']
    search_fields = ['question_text']

    #exclude = ('pub_date',)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

    exclude = ('correct_answer', 'selected_answer', 'correct')


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['title_text']}),
        ('Quiz description',    {'fields': ['quiz_text']}),
    ]
    inlines = [QuestionInline]

class AnswerSetAdmin(admin.ModelAdmin):
    fieldsets = []

admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerSet, AnswerSetAdmin)
